"""NAS interactions specific to imaging data."""
import os
import re
import time
from pathlib import Path

import numpy as np
import tifffile
import zarr
from tqdm import tqdm
from tifffile.tifffile import TiffFileError

from labnas.remote.base import SftpNas
from labnas.local.base import identify_tif_origin, TifFileMissingException
from labnas.local.base import assert_single_stack, sort_tif_files

SPLIT_PATTERN = "_[zt][0-9]+_"
TRIM_PATTERN = "[0-9]{2}.[0-9]{2}.[0-9]{2}.[0-9]+/"


def trim_path(remote_path: Path) -> Path:
    """Remove IP address etc from a remote path."""
    string = str(remote_path)
    if re.findall(TRIM_PATTERN, string):
        sub_string = re.split(TRIM_PATTERN, string)[-1]
        new_path = Path(sub_string)
        return new_path
    else:
        return remote_path


class ImagingNas(SftpNas):
    """Extends SftpNas for imaging data."""

    def sort_folder(
            self,
            remote_folder: Path,
            local_temp_folder: Path,
            remote_trash_folder: Path,
            recursive: bool = True,
            level: int = 0,
            save_one_up: bool = False,
    ) -> None:
        """Sort a folder with imaging .tif files.

        Currently only works for 2p data.
        """
        remote_folder = trim_path(remote_folder)
        remote_trash_folder = trim_path(remote_trash_folder)
        self.logger.info(f"=> Investigating: {remote_folder} (Level: {level})")
        if "INCOMPLETE" in remote_folder.name:
            self.logger.info(f"Skipping {remote_folder} -> INCOMPLETE flag.")
        elif "multipage" in remote_folder.name:
            self.logger.info(f"Skipping {remote_folder} -> multipage flag.")
        else:
            stacks, single_tifs = self.check_folder_structure(remote_folder)
            for stack_name, stack_tifs in stacks.items():
                self.process_stack(
                    stack_name=stack_name,
                    stack_tifs=stack_tifs,
                    remote_folder=remote_folder,
                    local_temp_folder=local_temp_folder,
                    remote_trash_folder=remote_trash_folder,
                    save_one_up=save_one_up,
                )
            if recursive:
                _, folders = self.list_files_and_folders(remote_folder)
                for folder in folders:
                    self.sort_folder(
                        remote_folder=folder,
                        local_temp_folder=local_temp_folder,
                        remote_trash_folder=remote_trash_folder,
                        level=level + 1,
                        save_one_up=save_one_up,
                    )

    def check_folder_structure(self, remote_folder: Path) -> tuple[dict, list]:
        """
        Check if a folder contains .tif files belonging to more than 1 stack.
        Also return stacks and tifs because scanning large folders takes time.
        """
        tifs = self.find_tifs_in_folder(remote_folder)
        if len(tifs) == 0:
            self.logger.info(f"No tifs in {remote_folder}.")
            stacks = {}
            single_tifs = []
        elif len(tifs) == 1:
            self.logger.info(f"Only 1 tif: {tifs[0]}.")
            stacks = {}
            single_tifs = tifs
        else:
            self.logger.info(f"{len(tifs)} tifs in {remote_folder}.")
            stacks, single_tifs = self.identify_stacks_in_tifs(tifs)
        return stacks, single_tifs

    def find_tifs_in_folder(self, remote_folder: Path) -> list[Path]:
        """Find tif files in a remote folder."""
        files, folders = self.list_files_and_folders(remote_folder)
        tifs = self.identify_tifs_in_files(files)
        return tifs

    @staticmethod
    def identify_tifs_in_files(files: list[Path]) -> list[Path]:
        """
        Identify tif files in a list of files.
        Pretty basic check for file extension.
        """
        tifs = []
        for file in files:
            if file.suffix in [".tif", ".tiff"]:
                tifs.append(file)
        return tifs

    def identify_stacks_in_tifs(self, tifs: list[Path], catch_error: bool = True) -> tuple[dict, list]:
        """Identify if tifs come from multi-frame recordings or if they are single snapshots."""
        self.logger.info("Looking for stacks.")
        try:
            tif_origin = identify_tif_origin(tifs[0])
        except ValueError as ve:
            if not catch_error:
                raise ve
            tif_origin = "unknown"

        self.logger.info(f"File name example: {tifs[0].name}")
        self.logger.info(f"Tif origin: {tif_origin}")
        if tif_origin == "leica":
            stacks, single_tifs = self.identify_leica_stacks_in_tifs(tifs)
        elif tif_origin == "basler":
            stacks, single_tifs = self.identify_basler_stacks_in_tifs(tifs)
        elif tif_origin == "leica_metadata":
            single_tifs = tifs
            stacks = {}
        else:
            self.logger.info(f"Could not identify tif origin: neither leica nor basler.")
            single_tifs = tifs
            stacks = {}
        self.logger.info(f"{len(stacks)} tif stack(s) and {len(single_tifs)} single tif(s) found.")
        return stacks, single_tifs

    def identify_leica_stacks_in_tifs(self, tifs: list[Path]) -> tuple[dict, list]:
        """Sort tif files into stacks belonging to a single recording."""
        stacks = {}
        single_tifs = []
        for file in tifs:
            file_name = file.name
            findings = re.findall(SPLIT_PATTERN, file_name)
            if findings:
                splitter = findings[0]
                parts = file_name.split(splitter)
                stack_name = parts[0]
                if stack_name not in stacks.keys():
                    self.logger.info(f"Stack in {tifs[0].parent}: {stack_name}")
                    stacks[stack_name] = []
                stacks[stack_name].append(file)
            else:
                single_tifs.append(file)
        stacks, single_tifs = self.check_for_false_stacks(stacks, single_tifs)
        return stacks, single_tifs

    def check_for_false_stacks(self, stacks: dict, single_tifs: list) -> tuple:
        """Check for stacks that only contain 1 tif (so they aren't really stacks after all)."""
        keys_to_delete = []
        for stack_name, stack_list in stacks.items():
            if len(stack_list) == 1:
                single_tifs.append(stack_list[0])
                keys_to_delete.append(stack_name)
                self.logger.info(f"Only 1 tif in stack {stack_name} -> Appending to single tifs.")
        for key in keys_to_delete:
            del stacks[key]
        return stacks, single_tifs

    def identify_basler_stacks_in_tifs(self, tifs: list[Path]) -> tuple[dict, list]:
        """Sort tif files into stacks belonging to a single recording."""
        stacks = {}
        single_tifs = []
        for file in tifs:
            parts = file.name.split("_")
            index_part = parts[-1]
            stack_name = "_".join(parts[:-1])
            if stack_name not in stacks.keys():
                stacks[stack_name] = []
            stacks[stack_name].append(file)
        stacks, single_tifs = self.check_for_false_stacks(stacks, single_tifs)
        return stacks, single_tifs

    def process_stack(
            self,
            stack_name: str,
            stack_tifs: list,
            remote_folder: Path,
            local_temp_folder: Path,
            remote_trash_folder: Path,
            save_one_up: bool,
    ) -> None:
        """
        TODO: split this
        1. Download stack as multipage tif.
        2. Upload multipage tif.
        3. Delete local multipage tif.
        4. Delete nas stack tifs.
        """
        # set paths
        if save_one_up:
            file_name = f"{remote_folder.name}_{stack_name}.tif"
            self.logger.info(f"Using parent folder and stack name as file name: {file_name}.")
            remote_tif = remote_folder.parent / "multipage_tiff" / file_name
            self.logger.info(f"Saving multipage-tiff one level up: {remote_tif}")
        else:
            remote_tif = remote_folder / "multipage_tiff" / f"{stack_name}.tif"
        self.logger.info(f"---{remote_tif}---")
        if self.is_file(remote_tif):
            raise FileExistsError(f"{remote_tif}")
        if not self.is_dir(remote_tif.parent):
            self.create_empty_folder(remote_tif.parent)
            self.logger.info(f"{remote_tif.parent} created.")
        self.logger.info(f"Downloading {stack_name} as as single tif.")

        trash_name = remote_folder / stack_name
        trash_name = str(trash_name).replace("/", "_")
        stack_trash_folder = remote_trash_folder / trash_name
        if self.is_file(stack_trash_folder):
            raise FileExistsError(f"{stack_trash_folder}")

        try:
            # 1. Download stack as multipage tif
            local_tif = self.download_files_as_single_tif(
                tif_files=stack_tifs,
                file_name=f"{stack_name}.tif",
                local_folder=local_temp_folder,
            )

            # 2. Upload multipage tif
            self.logger.info(f"Uploading {local_tif}")
            self.upload_file(local_tif, remote_tif)
            self.logger.info(f"Uploaded {local_tif} as {remote_tif}")

            # 3. Delete local multipage tif
            self.safely_delete(local_tif)

            # 4. Move stack tifs to trash
            self.create_empty_folder(stack_trash_folder)
            self.logger.info(f"Moving stack tifs to {stack_trash_folder}")
            for file in tqdm(stack_tifs):
                trash_path = stack_trash_folder / file.name
                self.move_file(file, trash_path)
        except (TifFileMissingException, TiffFileError) as e:
            self.logger.error(f"{e}")
            self.logger.info("Moving tifs into separate folder instead of combining.")
            incomplete_target = remote_folder / f"INCOMPLETE_{stack_name}"
            self.create_empty_folder(incomplete_target)
            self.logger.info(f"Moving stack tifs to {incomplete_target}")
            for file in tqdm(stack_tifs):
                new_path = incomplete_target / file.name
                self.move_file(file, new_path)

    def safely_delete(self, local_tif: Path, n_attempts: int = 3) -> bool:
        count = 0
        successful = False
        while count < n_attempts:
            try:
                os.remove(local_tif)
                self.logger.info(f"Removed {local_tif}")
                successful = True
                break
            except PermissionError as pe:
                self.logger.info(f"Could not remove {local_tif} on attempt {count + 1}: {pe}")
                time.sleep(10)
                count += 1
        if not successful:
            self.logger.warning(f"Failed to remove {local_tif} after {count} attempts.")
        return successful

    def create_folder_for_stack(self, stack_name: str, remote_folder: Path, stack_files: list[Path]) -> None:
        """Move .tif files belonging to a single stack into a dedicated folder."""
        self.logger.info(f"{len(stack_files)} tifs in stack {stack_name}.")
        parent_directory = remote_folder / stack_name
        if parent_directory.is_dir():
            raise FileExistsError(f"{parent_directory}")
        self.connection.mkdir(str(parent_directory))
        for file in tqdm(stack_files):
            new_path = parent_directory / file.name
            self.move_file(file, new_path)
        self.logger.info(f"Moved {len(stack_files)} tifs into {parent_directory}.")

    def download_files_as_single_tif(self, tif_files: list, file_name: str, local_folder: Path) -> Path:
        """Download multiple 2D tif files and combine to single 3D tif."""
        multipage_local = local_folder / file_name
        assert multipage_local.suffix == ".tif"
        n_files = len(tif_files)
        self.logger.info(f"{len(tif_files)} tif files")
        assert n_files > 1, f"Not enough files: {n_files=} < 1"
        assert_single_stack(tif_files)
        tif_files = sort_tif_files(tif_files, logger=self.logger)
        for i_file in tqdm(range(n_files)):
            image = self._read_frame_safely(tif_files, i_file, local_folder)
            if i_file == 0:
                z = self._create_empty_storage(n_files, image, multipage_local)
            z[i_file, :, :] = image
        os.remove(local_folder / "temp.tif")
        return multipage_local

    def download_folder_as_single_tif(self, remote_folder: Path, local_folder: Path) -> Path:
        """Download each tif of a stack, save into a singe local tif."""
        multipage_local = local_folder / f"{remote_folder.name}.tif"
        tif_files = self.find_tifs_in_folder(remote_folder)
        n_files = len(tif_files)
        self.logger.info(f"{len(tif_files)} tif files in {remote_folder}")
        assert n_files > 1, f"Not enough files in {remote_folder}: {n_files} < 1"
        assert_single_stack(tif_files)
        tif_files = sort_tif_files(tif_files)
        for i_file in tqdm(range(n_files)):
            image = self._read_frame_safely(tif_files, i_file, local_folder)
            if i_file == 0:
              z = self._create_empty_storage(n_files, image, multipage_local)
            z[i_file, :, :] = image
        os.remove(local_folder / "temp.tif")
        return multipage_local

    def _create_empty_storage(self, n_files: int, image: np.ndarray, target_file: Path) -> zarr.Array:
        """Create empty multipage tiff that can be filled iteratively."""
        shape = (n_files, image.shape[0], image.shape[1])
        tifffile.imwrite(
            target_file,
            shape=shape,
            dtype=np.uint8,
        )
        store = tifffile.imread(target_file, mode="r+", aszarr=True)
        z = zarr.open(store, mode="r+")
        self.logger.info(f"Empty tif created: {shape}")
        return z

    def _read_frame_safely(self, tif_files: np.ndarray, i_file: int, local_folder: Path) -> np.ndarray:
        """
        Read a single frame TIFF and return contents.
        In case it is corrupted, reconstruct from previous and next.
        """
        temp_local = local_folder / "temp.tif"
        file = tif_files[i_file]
        self.download_file(file, temp_local, overwrite=True)
        try:
            image = tifffile.imread(temp_local)
            assert image.ndim == 2, f"{file} is not 2D"
            assert image.shape[0] > 0, f"{file}: {image.shape[0]=} is invalid"
            assert image.shape[1] > 0, f"{file}: {image.shape[1]=} is invalid"
        except tifffile.tifffile.TiffFileError as e:
            self.logger.error(f"Cannot read {file}: {e}")
            image = self._fill_in_corrupted(tif_files, i_file, local_folder)
            self.logger.info(f"Reconstructed {file} from previous and next frame.")
        except AssertionError as e:
            self.logger.info(f"Image data in {file} is erroneous")
            self.logger.info(f"Error: {e}")
            image = self._fill_in_corrupted(tif_files, i_file, local_folder)
            self.logger.info(f"Reconstructed {file} from previous and next frame.")
        return image


    def _fill_in_corrupted(self, tif_files: np.ndarray, i_file: int, local_folder: Path) -> np.ndarray:
        """
        In case a single frame is corrupted, we can replace it with the average of the prev and the next frame.
        Notes:
            - avg will have noticeably less noise than real frames
            - will fail if
                - missing tif is either at the start or end of recording
                - there are consecutive corrupted tiffs
        """
        prev_file = tif_files[i_file - 1]
        next_file = tif_files[i_file + 1]
        temp_local_prev = local_folder / "temp_prev.tif"
        temp_local_next = local_folder / "temp_next.tif"
        self.download_file(prev_file, temp_local_prev, overwrite=True)
        self.download_file(next_file, temp_local_next, overwrite=True)
        prev_img = tifffile.imread(temp_local_prev)
        next_img = tifffile.imread(temp_local_next)
        surrounding_images = np.stack([prev_img, next_img], axis=0)
        avg = np.mean(surrounding_images, axis=0)
        return avg

