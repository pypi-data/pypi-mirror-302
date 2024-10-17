"""
Automatically create and maintain recording database.

TODO:
In separate script:
- find metadata for each tif
- extract tif metadata

In this script:
- get timestamps of tif and stim
- associate tif with stim

In eyetracking:
- get pupil positions, motion energy
"""
import configparser
import os
import datetime
from pathlib import Path

import numpy as np
import pandas as pd

from labnas.remote.imaging import ImagingNas
from labnas.remote.utils import transfer_file
from labnas.remote.auto_dset.utils import scan_multipage_tiffs, check_file_name_for_disqualifiers, check_file_name_with_list
from labnas.remote.auto_dset.metadata import find_metadata_file, extract_metadata_info, get_empty_metadata_info
from labnas.remote.auto_dset.stim import get_timestamp, extract_stim_info, get_empty_stim_info
from labnas.remote.auto_dset.suite2p import extract_suite2p_info, get_empty_suite2p_info

ALLOWED_SESSIONS = [
    "flashes",
    "cfs",
    "conflict",
    "alternations",
    "ori",
    # "scouting"
]


class TwophotonDatabase:
    """Create and maintain 2p recording database."""
    def __init__(
            self,
            raw_base: Path,
            processed_base: Path,
            target_base: Path,
            raw_nas: ImagingNas,
            processed_nas: ImagingNas,
            temp_local: Path,
            recheck: bool = False,
    ) -> None:
        # params
        self.raw_base = raw_base
        self.processed_base = processed_base
        self.dset_base = target_base
        self.raw_nas = raw_nas
        self.processed_nas = processed_nas
        self.temp_local = temp_local
        self.should_recheck = recheck

        # other
        self.tif_files = []
        self.stim_types = []
        self.dataset_names = []
        self.database_table: pd.DataFrame | None = None

        #
        self.current_recording = {}
        self.is_in_table = False

    def run(self) -> None:
        """Main method to call."""
        self.find_recording_tifs()
        self.load_database_table()
        self.update_database()
        self.save_database_table()

    def find_recording_tifs(self) -> None:
        """Look for 2p recording tifs that could be the basis of a dataset"""
        print(f"Looking for multipage tiffs in {self.raw_base}")
        tif_candidates = scan_multipage_tiffs(self.raw_base, self.raw_nas)
        print(f"TIFFs in multipage folders: {len(tif_candidates)}")
        selected = []
        stim_types = []
        for file in tif_candidates:
            file_name = file.name
            is_ok = check_file_name_for_disqualifiers(file_name)
            is_relevant, stim_type = check_file_name_with_list(file_name, ALLOWED_SESSIONS)
            if is_ok & is_relevant:
                selected.append(file)
                stim_types.append(stim_type)
        print(f"Selected TIFFs for auto-dset: {len(selected)}")
        self.tif_files = selected
        self.stim_types = stim_types

    def load_database_table(self) -> None:
        """Load the old database file."""
        csv_file = self.dset_base / "database.csv"
        if self.processed_nas.is_file(csv_file):
            local_copy = self.temp_local / csv_file.name
            self.processed_nas.download_file(csv_file, local_copy, overwrite=True)
            self.database_table = pd.read_csv(local_copy)
            os.remove(local_copy)
            print(f"Entries in database: {self.database_table.shape[0]}")
        else:
            print(f"Could not load database file: {csv_file} does not exist.")

    def update_database(self) -> None:
        """Iterate over all tifs."""
        for file, stim_type in zip(self.tif_files, self.stim_types):
            self.check_single_recording(file, stim_type)

    def check_single_recording(self, tif_file: Path, stim_type: str) -> None:
        """For a single recording, try to create / maintain a dataset folder."""
        # reset
        self.current_recording = {}  # reset
        self.is_in_table = False

        # let's go
        self.get_dset_name(tif_file, stim_type)
        print(f"---{self.current_recording['dset_name']}---")
        self.check_entry()
        self.collect_dataset()
        self.save_txt()


    def get_dset_name(self, tif_file: Path, stim_type: str) -> str:
        """Get a unique name for a recording."""
        count = 0
        mouse_name = tif_file.parts[3]
        date_string = tif_file.parts[4]
        short_date = date_string.replace("-", "")

        self.current_recording["date"] = date_string
        self.current_recording["mouse"] = mouse_name
        self.current_recording["stim_type"] = stim_type
        self.current_recording["tif_file"] = tif_file
        self.current_recording["tif_stem"] = tif_file.stem

        dataset_name = f"{short_date}_{mouse_name}_{stim_type}_{count}"
        if dataset_name in self.dataset_names:
            while dataset_name in self.dataset_names:
                count += 1
                dataset_name = f"{short_date}_{mouse_name}_{stim_type}_{count}"
        self.dataset_names.append(dataset_name)
        self.current_recording["dset_name"] = dataset_name
        return dataset_name

    def check_entry(self) -> None:
        dataset_name = self.current_recording["dset_name"]
        if self.database_table is not None:
            if dataset_name in self.database_table["dset_name"].values:
                self.is_in_table = True
                print(f"Database: entry already exists.")
            else:
                self.is_in_table = False
                print(f"Database: no entry found.")

    def collect_dataset(self) -> None:
        """Check what files exist for a recording."""
        self.create_dataset_folder()
        print(f"TIF file: {self.current_recording['tif_file']}")
        self.collect_metadata()
        self.collect_suite2p()
        self.collect_stim()

    def create_dataset_folder(self) -> None:
        """Check whether dataset in database folder."""
        dset_name = self.current_recording["dset_name"]
        dset_folder = self.dset_base / dset_name
        if not self.processed_nas.is_dir(dset_folder):
            print("Creating database folder.")
            self.processed_nas.create_empty_folder(dset_folder)
        self.current_recording["dset_folder"] = dset_folder
        print(f"Database folder: {dset_folder}")

    def collect_metadata(self) -> None:
        """Collect leica metadata files and info."""
        try:
            source = self.find_metadata()
        except FileNotFoundError as e:
            source = None
            print(f"Metadata file not found: {e}")

        if source is not None:
            self.transfer_metadata(source)
            if (not self.is_in_table) or self.should_recheck:
                self.extract_metadata()
        else:
            metadata_info = get_empty_metadata_info()
            for key, val in metadata_info.items():
                self.current_recording[f"metadata_{key}"] = val

    def find_metadata(self) -> Path:
        # find raw leica metadata
        tif_file = self.current_recording["tif_file"]
        source_file = find_metadata_file(tif_file, self.raw_nas)
        print(f"Metadata source file: {source_file}")
        return source_file

    def transfer_metadata(self, source_file: Path) -> None:
        target_file = self.current_recording["dset_folder"] / "raw" / "tif_metadata.xml"
        if not self.processed_nas.is_dir(target_file.parent):
            self.processed_nas.create_empty_folder(target_file.parent)
            print("Creating raw folder in database.")
        if not self.processed_nas.is_file(target_file):
            print(f"Transferring {source_file} to {target_file}")
            transfer_file(
                source_nas=self.raw_nas,
                source_file=source_file,
                target_nas=self.processed_nas,
                target_file=target_file,
                local_temp=self.temp_local,
            )
        print(f"Metadata file in database: {target_file}")

    def extract_metadata(self) -> None:
        target_file = self.current_recording["dset_folder"] / "raw" / "tif_metadata.xml"
        metadata_info = extract_metadata_info(target_file, self.processed_nas, self.temp_local)
        for key, val in metadata_info.items():
            self.current_recording[f"metadata_{key}"] = val

    def collect_suite2p(self) -> None:
        """Check whether files related to ROI extraction exist."""
        try:
            source = self.find_suite2p()
        except FileNotFoundError:
            source = None
            print("Suite2p data: no source found.")

        if source is not None:
            self.transfer_suite2p(source)
            if (not self.is_in_table) or self.should_recheck:
                self.extract_suite2p()
        else:
            suite2p_info = get_empty_suite2p_info()
            for key, val in suite2p_info.items():
                self.current_recording[f"suite2p_{key}"] = val


    def find_suite2p(self) -> Path:
        # find files in source
        date_folder = self.processed_base / "suite2p" / self.current_recording["mouse"] / self.current_recording["date"]
        if not self.processed_nas.is_dir(date_folder):
            raise FileNotFoundError(f"{date_folder}")
        source_folder = date_folder / self.current_recording["tif_stem"]
        if not self.processed_nas.is_dir(source_folder):
            raise FileNotFoundError(f"{source_folder}")
        print(f"Suite2p data found: {source_folder}")
        return source_folder

    def transfer_suite2p(self, source: Path) -> None:
        # check whether files are in database
        target_folder = self.current_recording["dset_folder"] / "suite2p"
        if not self.processed_nas.is_dir(target_folder):
            print("Copying suite2p data to database.")
            self.processed_nas.copy_folder(source, target_folder, self.temp_local)
        print(f"Suite2p in database: {target_folder}")

    def extract_suite2p(self) -> None:
        # extract some info
        target_folder = self.current_recording["dset_folder"] / "suite2p"
        suite2p_info = extract_suite2p_info(target_folder, self.processed_nas, self.temp_local)
        for key, val in suite2p_info.items():
            self.current_recording[f"suite2p_{key}"] = val


    def collect_stim(self) -> None:
        """Check whether a table with stimulus information per 2p frame has been created."""
        try:
            self.transfer_stim()
            if (not self.is_in_table) or self.should_recheck:
                self.extract_stim()
        except FileNotFoundError:
            stim_info = get_empty_stim_info()
            for key, val in stim_info.items():
                self.current_recording[f"stim_{key}"] = val

    def transfer_stim(self) -> None:
        # check whether files are in database
        date_folder = self.processed_base / "stim" / self.current_recording["mouse"] / self.current_recording["date"]
        if not self.processed_nas.is_dir(date_folder):
            raise FileNotFoundError(f"{date_folder}")
        target_file = self.current_recording["dset_folder"] / "frame_info.csv"
        if not self.processed_nas.is_file(target_file):
            # transfer (it gets a bit complicated)
            print("Frame info: No file yet.")
            source_file = self._find_stim_in_date(date_folder)  # this requires downloading files
            print("Frame info: Copying file to database.")
            self.processed_nas.copy_file(
                remote_source=source_file,
                remote_target=target_file,
                local_temp=self.temp_local,
            )
        print(f"Frame info in database: {target_file}")

    def extract_stim(self) -> None:
        target_file = self.current_recording["dset_folder"] / "frame_info.csv"
        info = extract_stim_info(target_file, self.processed_nas, self.temp_local)
        for key, val in info.items():
            self.current_recording[f"stim_{key}"] = val

    def _find_stim_in_date(self, folder: Path) -> Path:
        """Find the frame info file corresponding to the recording tif."""
        print("Looking for corresponding frame info files.")
        tif_timestamp = self._get_metadata_timestamp()
        candidates = self._find_frame_info_files(folder)
        stim_file = self._find_closest_frame_info(tif_timestamp, candidates)
        return stim_file

    def _get_metadata_timestamp(self) -> datetime.datetime:
        """Get the timestamp of the recording start from the Leica metadata file."""
        metadata_file = self.current_recording["dset_folder"] / "raw" / "tif_metadata.xml"
        metadata_info = extract_metadata_info(metadata_file, self.processed_nas, self.temp_local)
        timestamp = metadata_info["timestamp_start"]
        print(f"Metadata timestamp: {timestamp}")
        return timestamp

    def _find_frame_info_files(self, date_folder: Path) -> list:
        """Find frame info files in a folder."""
        _, folders = self.processed_nas.list_files_and_folders(date_folder)
        candidates = []
        for folder in folders:
            frame_info_file = folder / "frame_info.csv"
            if self.processed_nas.is_file(frame_info_file):
                candidates.append(frame_info_file)
        print(f"Frame info: {len(candidates)} candidate files found.")
        assert len(candidates) > 0
        for candidate in candidates:
            print(f"\t {candidate.parent.name}")
        return candidates

    def _find_closest_frame_info(self, tif_timestamp: datetime.datetime, candidates: list) -> Path:
        """Identify which of the frame info files from the same session fits to this particular tif."""
        diffs = []
        for file in candidates:
            stim_timestamp = get_timestamp(
                remote_file=file,
                nas=self.processed_nas,
                local_temp=self.temp_local,
            )
            delta = tif_timestamp - stim_timestamp
            delta = delta.total_seconds()
            diffs.append(delta)
        abs_diffs = np.abs(diffs)
        min_delta = np.min(abs_diffs)
        i_min = np.argmin(abs_diffs)
        stim_file = candidates[i_min]
        print(f"Frame info: {stim_file.parent.name} has smallest offset to tif timestamp ({min_delta:.3f}s)")
        return stim_file

    def save_txt(self) -> None:
        """Create an overview .txt file for the user to read out basic information about the recording."""
        target_file = self.current_recording["dset_folder"] / "overview.txt"
        if (not self.is_in_table) or self.should_recheck:
            # single overview
            print("Creating overview file.")
            config = configparser.ConfigParser()
            str_dict = {key: str(val) for key, val in self.current_recording.items()}
            config.read_dict({"basics": str_dict})
            file_path = self.temp_local / "overview.txt"
            with open(file_path, "w") as file:
                config.write(file)
            try:
                self.processed_nas.upload_file(file_path, target_file, overwrite_remote=True)
            except OSError as e:
                print(f"Failed to upload txt file: {e}")
        else:
            assert self.processed_nas.is_file(target_file)
        print(f"Overview file: {target_file}")

        # save to table
        local_table = self.temp_local / "database.csv"
        df = pd.DataFrame([self.current_recording])
        if local_table.is_file():
            df.to_csv(local_table, mode="a", header=False)
        else:
            df.to_csv(local_table)

    def save_database_table(self) -> None:
        raise NotImplementedError()  # todo: compare new entries to old
        local_table = self.temp_local / "database.csv"
        remote_target = self.dset_base / "database.csv"
        self.processed_nas.upload_file(local_table, remote_target, overwrite_remote=True)
