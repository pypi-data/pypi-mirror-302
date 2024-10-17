"""Basic connection to a network-associated server (NAS)."""
import logging
import os
import sys
from pathlib import Path, PurePath, PurePosixPath

import pysftp
from tqdm import tqdm


PathLike = Path | PurePath


class SftpNas:
    """Basic SFTP connection (wrapper around pysftp)"""

    def __init__(
            self,
            host_name: str,
            user_name: str,
            pwd: str,
            log_file: Path | None = None,
            logger: logging.Logger | None = None
    ) -> None:
        """Create pysftp.Connection to server."""
        # params
        self._host_name = host_name
        self._user_name = user_name
        self._pwd = pwd
        self.logger = logger
        self.log_file = log_file

        # state
        self.is_open: bool = False
        self.connection: pysftp.Connection | None = None

        # go
        if self.logger is None:
            self.logger = self.create_logger()
        self._establish_connection()

    def _establish_connection(self, verbose: bool = True) -> None:
        """Establish an SFTP connection."""
        if self.is_open:
            raise ValueError(f"SFTP connection is already open!")
        self.connection: pysftp.Connection = pysftp.Connection(
            host=self._host_name,
            username=self._user_name,
            password=self._pwd,
        )
        if verbose:
            self.logger.info(f"Connection established: {self._host_name}@{self._user_name}")
        self.is_open = True

    def create_logger(self) -> logging.Logger:
        """Create a logger to print output to. Optionally save output to file."""
        logger = logging.Logger("nas")
        logger.setLevel(logging.DEBUG)
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter("%(asctime)s - %(message)s")
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
        if isinstance(self.log_file, Path):
            file_handler = logging.FileHandler(self.log_file)
            formatter = logging.Formatter("%(asctime)s - %(message)s")
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
            logger.info(f"NAS log file: {self.log_file}")
        return logger

    def close_connection(self, verbose: bool = True) -> None:
        """Close SFTP connection."""
        self.connection.close()
        self.is_open = False
        if verbose:
            self.logger.info(f"Connection closed: {self._host_name}@{self._user_name}")

    def reconnect(self, verbose: bool = False) -> None:
        """Attempt to re-establish pysftp.Connection."""
        assert self.is_open
        self.logger.info(f"Reconnecting {self._host_name}@{self._user_name}.")
        self.close_connection(verbose=verbose)
        self._establish_connection(verbose=verbose)

    def list_contents(self, remote_folder: PathLike) -> list[PathLike]:
        """List contents of a NAS folder"""
        remote_folder = self._convert_to_linux(remote_folder)
        if not self.is_dir(remote_folder):
            raise FileNotFoundError(f"{remote_folder} not found.")
        contents: list[str] = self.connection.listdir(str(remote_folder))
        contents: list[PathLike] = [remote_folder / name for name in contents]
        return contents

    def is_dir(self, remote_path: PathLike) -> bool:
        """Check whether a NAS path is a directory."""
        remote_path = self._convert_to_linux(remote_path)
        return self.connection.isdir(str(remote_path))

    def list_files_and_folders(self, remote_folder: PathLike) -> tuple:
        """List contents of a NAS folder sorted into files and folders"""
        files = []
        folders = []
        remote_folder = self._convert_to_linux(remote_folder)
        contents = self.list_contents(remote_folder)
        for element in contents:
            if self.is_file(element):
                files.append(element)
            elif self.is_dir(element):
                folders.append(element)
            else:
                raise ValueError(f"{element} is neither file nor folder?")
        return files, folders

    def list_files(self, remote_folder: PathLike) -> list:
        """Convenience method to only list files in a remote folder."""
        files, _ = self.list_files_and_folders(remote_folder)
        return files

    def list_folders(self, remote_folder: PathLike) -> list:
        """Convenience method to only list folders in a remote folder."""
        _, folders = self.list_files_and_folders(remote_folder)
        return folders

    def is_file(self, remote_path: PathLike) -> bool:
        """Check whether a NAS path is a file."""
        remote_path = self._convert_to_linux(remote_path)
        return self.connection.isfile(str(remote_path))

    def download_file(self, remote_file: Path, local_file: Path, overwrite: bool = False) -> None:
        """Download a single file from the server"""
        remote_file = self._convert_to_linux(remote_file)
        if not self.is_file(remote_file):
            raise FileNotFoundError(f"{remote_file} does not exist.")
        if not local_file.parent.is_dir():
            raise FileNotFoundError(f"Target parent folder {local_file.parent} does not exist.")
        if local_file.is_file() and not overwrite:
            raise FileExistsError(f"{local_file} already exists.")
        self.connection.get(str(remote_file), str(local_file))

    def upload_file(self, local_file: Path, remote_file: Path, overwrite_remote: bool = False) -> None:
        """Upload a single file to the server"""
        remote_file = self._convert_to_linux(remote_file)
        if not local_file.is_file():
            raise FileNotFoundError(f"{local_file} does not exist.")
        if not self.is_dir(remote_file.parent):
            raise FileNotFoundError(f"Target parent folder {remote_file.parent} does not exist.")
        if self.is_file(remote_file):
            if overwrite_remote:
                self.delete_file(remote_file)
                self.logger.info(f"{remote_file} already exists -> deleted.")
            else:
                raise FileExistsError(f"{remote_file} already exists.")
        self.connection.put(str(local_file), str(remote_file))

    def download_folder(self, remote_folder: Path, local_parent: Path, recursive: bool = True, verbose: bool = True) -> Path:
        """Download a whole folder from the server"""
        remote_folder = self._convert_to_linux(remote_folder)
        if not self.is_dir(remote_folder):
            raise FileNotFoundError(f"{remote_folder} does not exist.")
        if not local_parent.is_dir():
            raise FileNotFoundError(f"Target parent folder {local_parent} does not exist.")
        local_folder = local_parent / remote_folder.name
        if local_folder.is_dir():
            raise FileExistsError(f"{local_folder} already exists.")
        os.mkdir(local_folder)
        files, folders = self.list_files_and_folders(remote_folder)
        if verbose:
            self.logger.info(f"{len(files)} files found in {remote_folder}.")
            self.logger.info(f"{len(folders)} folders found in {remote_folder}.")
            for remote_file in tqdm(files):
                local_file = local_folder / remote_file.name
                self.download_file(remote_file, local_file)
        else:
            for remote_file in files:
                local_file = local_folder / remote_file.name
                self.download_file(remote_file, local_file)
        if recursive:
            for remote_sub_folder in folders:
                self.download_folder(remote_sub_folder, local_folder, recursive=recursive, verbose=verbose)
        return local_folder

    def upload_folder(
            self,
            local_source: Path,
            remote_parent: PathLike,
            recursive: bool = True,
            make_tree: bool = False,
            remote_name: str | None = None,
            verbose: bool = True,
    ) -> PathLike:
        """Upload a folder to the NAS"""
        remote_parent = self._convert_to_linux(remote_parent)
        if not local_source.is_dir():
            raise FileNotFoundError(f"{local_source} does not exist.")
        if not self.is_dir(remote_parent):
            if make_tree:
                self.connection.makedirs(str(remote_parent))
                self.logger.info(f"Folder tree to {remote_parent} created.")
            else:
                raise FileNotFoundError(f"{remote_parent} does not exist.")

        # create nas folder
        if isinstance(remote_name, str):
            remote_target = remote_parent / remote_name
        else:
            remote_target = remote_parent / local_source.name
        if self.connection.isdir(str(remote_target)):
            raise FileExistsError(f"{remote_target} already exists.")
        self.connection.mkdir(str(remote_target))
        if verbose:
            self.logger.info(f"Remote folder {remote_target} created.")

        # get contents of local folder
        elements = list(local_source.iterdir())
        files = []
        folders = []
        for element in elements:
            if element.is_file():
                files.append(element)
            elif element.is_dir():
                folders.append(element)

        # upload files
        for local_file in files:
            remote_file = remote_target / local_file.name
            self.upload_file(local_file, remote_file)
            if verbose:
                self.logger.info(f"{local_file} -> {remote_file}")

        # upload sub-folders
        if recursive:
            for local_sub_folder in folders:
                self.upload_folder(local_sub_folder, remote_target, verbose=verbose)
        return remote_target

    def move_file(self, remote_source: Path, remote_target: Path) -> None:
        """Move a remote file to another remote location.."""
        remote_source = self._convert_to_linux(remote_source)
        remote_target = self._convert_to_linux(remote_target)
        if not self.is_file(remote_source):
            raise FileNotFoundError(f"{remote_source}")
        if self.is_file(remote_target):
            raise FileExistsError(f"{remote_target}")
        if not self.is_dir(remote_target.parent):
            raise FileNotFoundError(f"{remote_target.parent}")
        self.connection.rename(str(remote_source), str(remote_target))

    def move_folder(self, remote_source: Path, remote_target: Path) -> None:
        """Move a folder from one nas location to another."""
        remote_source = self._convert_to_linux(remote_source)
        remote_target = self._convert_to_linux(remote_target)
        if not self.is_dir(remote_source):
            raise FileNotFoundError(f"{remote_source} does not exist.")
        if self.is_dir(remote_target):
            raise FileExistsError(f"{remote_target} already exists.")
        self.connection.rename(str(remote_source), str(remote_target))

    def copy_file(
            self,
            remote_source: Path,
            remote_target: Path,
            local_temp: Path,
            overwrite_temp: bool = True,
            overwrite_remote: bool = False,
    ) -> None:
        """
        Copy a remote file to another remote location.
        This requires downloading & uploading the file which is inefficient.
        """
        remote_source = self._convert_to_linux(remote_source)
        remote_target = self._convert_to_linux(remote_target)
        if not self.is_file(remote_source):
            raise FileNotFoundError(f"{remote_source=} does not exist.")
        if self.is_file(remote_target):
            if overwrite_remote:
                self.delete_file(remote_target)
            else:
                raise FileExistsError(f"{remote_target=} already exists.")
        if not self.is_dir(remote_target.parent):
            raise FileNotFoundError(f"Target parent {remote_target.parent} does not exist.")
        local_copy = local_temp / remote_source.name
        self.download_file(remote_source, local_copy, overwrite=overwrite_temp)
        self.upload_file(local_copy, remote_target)
        os.remove(local_copy)

    def copy_folder(self, remote_source: Path, remote_target: Path, local_temp: Path, overwrite_remote: bool = False) -> None:
        """
        Copy a remote folder to another remote location.
        This requires downloading & uploading the files inside that folder which is inefficient.
        """
        if not self.is_dir(remote_source):
            raise FileNotFoundError(f"{remote_source=} does not exist.")
        if not self.is_dir(remote_target):
            # self.logger.info(f"Creating {remote_target=}")
            self.create_empty_folder(remote_target)
        files, folders = self.list_files_and_folders(remote_source)
        for file in files:
            self.copy_file(file, remote_target / file.name, local_temp=local_temp, overwrite_remote=overwrite_remote)
        for folder in folders:
            remote_sub = remote_target / folder.name
            if not self.is_dir(remote_sub):
                self.create_empty_folder(remote_sub)
                self.copy_folder(folder, remote_sub, local_temp, overwrite_remote=overwrite_remote)


    def create_empty_folder(self, remote_folder: Path) -> None:
        """Create empty folder on NAS."""
        remote_folder = self._convert_to_linux(remote_folder)
        if self.is_dir(remote_folder):
            raise FileExistsError(f"{remote_folder} already exists.")
        self.connection.makedirs(str(remote_folder))

    def get_file_size(self, remote_file: Path, unit: str = "gb") -> float:
        """Get size of a remote file."""
        remote_file = self._convert_to_linux(remote_file)
        stats = self.connection.stat(str(remote_file))
        file_size = stats.st_size
        if unit == "kb":
            file_size = file_size / 10 ** 3
        elif unit == "mb":
            file_size = file_size / 10 ** 6
        elif unit == "gb":
            file_size = file_size / 10 ** 9
        else:
            raise NotImplementedError(f"{unit=} not implemented")
        return file_size

    @staticmethod
    def _convert_to_linux(remote_path: Path) -> PurePosixPath:
        """
        Convert remote path to PurePosixPath.
        This is for Windows compatibility.
        """
        assert isinstance(remote_path, (Path, PurePath)), f"{remote_path} is not a Path but {type(remote_path)}"
        remote_path = PurePosixPath(remote_path)
        return remote_path

    def is_empty(self, remote_folder: Path) -> bool:
        """Check whether a remote folder is empty."""
        files, folders = self.list_files_and_folders(remote_folder)
        if (len(files) > 0) or (len(folders) > 0):
            return False
        else:
            return True

    def delete_file(self, remote_file: Path) -> None:
        """Delete a remote file."""
        if not self.is_file(remote_file):
            raise FileNotFoundError(f"{remote_file}")
        self.connection.remove((str(remote_file)))
        assert not self.is_file(remote_file)

    def delete_folder(self, remote_folder: Path) -> None:
        """Delete a remote folder recursively."""
        if not self.is_dir(remote_folder):
            raise FileNotFoundError(f"{remote_folder}")
        files, folders = self.list_files_and_folders(remote_folder)
        for file in files:
            self.delete_file(file)
        for folder in folders:
            self.delete_folder(folder)
        self.connection.rmdir(str(remote_folder))

