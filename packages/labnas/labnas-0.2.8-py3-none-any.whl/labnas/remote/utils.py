"""
Some utility functions for interactions with one or two NAS.
"""
import re
from configparser import ConfigParser
from pathlib import Path

import os
import shutil
from labnas.remote.base import SftpNas
from labnas.remote.imaging import ImagingNas



def get_nas_from_config(config_file: Path, nas_name: str, log_file: Path | None = None) -> ImagingNas:
    """Get NAS-object with params from a config file."""
    config = ConfigParser()
    config.read(config_file)
    nas = ImagingNas(
        host_name=config[nas_name]["host"],
        user_name=config[nas_name]["user"],
        pwd=config[nas_name]["pwd"],
        log_file=log_file,
    )
    return nas



def transfer_folder(source_nas: SftpNas, target_nas: SftpNas, source_folder: Path, target_folder: Path, local_temp: Path) -> None:
    """Transfer a folder from one NAS to another."""
    local_folder = local_temp / source_folder.name
    if local_folder.is_dir():
        shutil.rmtree(local_folder)
    source_nas.download_folder(source_folder, local_folder.parent, verbose=False)
    target_nas.upload_folder(local_folder, target_folder.parent, remote_name=target_folder.name, verbose=False)
    shutil.rmtree(local_folder)


def transfer_file(source_nas: SftpNas, target_nas: SftpNas, source_file: Path, target_file: Path, local_temp: Path) -> None:
    """Transfer a file from one NAS to another."""
    local_copy = local_temp / source_file.name
    if local_copy.is_file():
        os.remove(local_copy)
    source_nas.download_file(source_file, local_copy)
    target_nas.upload_file(local_copy, target_file)
    os.remove(local_copy)




def delete_if_empty(folder: Path, nas: SftpNas, trash: Path) -> None:
    """Delete a remote folder if it is empty."""
    if not nas.is_dir(folder):
        raise FileNotFoundError(f"{folder}")
    if nas.is_empty(folder):
        try:
            nas.delete_folder(folder)
        except Exception as e:
            print(f"Cannot delete folder: {e}")
            print("Attempting to move folder to trash instead.")
            trash_name = "_".join(folder.parts)
            trash_target = trash / trash_name
            nas.move_folder(folder, trash_target)
        print(f"{folder} deleted.")



def check_eyetracking(recording_folder: Path, nas: SftpNas) -> None:
    """Check whether a remote folder contains subfolders for right and left eye."""
    files, folders = nas.list_files_and_folders(recording_folder)
    has_right = False
    has_left = False
    right_size = None
    left_size = None
    for folder in folders:
        if folder.name == "right_eye":
            has_right = True
        elif folder.name == "left_eye":
            has_left = True
        sub_files, sub_folders = nas.list_files_and_folders(folder)
        for file in sub_files:
            # print(file)
            pass
        for f in sub_folders:
            print(f)
    if not has_right:
        raise FileNotFoundError(f"{recording_folder / 'right_eye'} does not exist.")
    if not has_left:
        raise FileNotFoundError(f"{recording_folder / 'left_eye'} does not exist.")
