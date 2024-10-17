"""
"""

import os
from datetime import datetime
from pathlib import Path

import pandas as pd

from labnas.remote.imaging import ImagingNas


TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def get_empty_stim_info() -> dict:
    stim_info = {
        "screen_flips": None,
        "timestamp_start": None,
        "timestamp_end": None,
        "duration_min": None,
    }
    return stim_info

def extract_stim_info(stim_folder: Path, nas: ImagingNas) -> dict:
    flip_file = _find_flip_file(stim_folder, nas)
    info = _extract_flip_info(flip_file, nas)
    return info


def _find_flip_file(stim_folder: Path, nas: ImagingNas) -> Path:
    files, folders = nas.list_files_and_folders(stim_folder)
    flip_file = None
    for file in files:
        if file.name == "flip_info.csv":
            flip_file = file
            break
    if flip_file is None:
        raise FileNotFoundError(f"No flip file in {stim_folder}")
    return flip_file


def _extract_flip_info(flip_file: Path, nas: ImagingNas, local_temp: Path) -> dict:
    """Read out basic info from a remote flip file."""
    local_copy = local_temp / flip_file.name
    if local_copy.is_file():
        os.remove(local_copy)
    nas.download_file(flip_file, local_copy)
    df = pd.read_csv(local_copy)
    if "datetime" in df.columns:
        first_timestamp = df["datetime"].values[0]
        last_timestamp = df["datetime"].values[-1]
        first_timestamp = datetime.strptime(first_timestamp, TIMESTAMP_FORMAT)
        last_timestamp = datetime.strptime(last_timestamp, TIMESTAMP_FORMAT)
        elapsed = last_timestamp - first_timestamp
        duration_minutes = elapsed.total_seconds() / 60
    else:
        raise KeyError(f"No 'datetime' in {flip_file}?")
    os.remove(local_copy)
    info = {
        "screen_flips": df.shape[0],
        "timestamp_start": first_timestamp,
        "timestamp_end": last_timestamp,
        "duration_min": duration_minutes,
    }
    return info

