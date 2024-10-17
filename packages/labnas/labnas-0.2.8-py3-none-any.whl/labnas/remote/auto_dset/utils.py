import datetime
import os
import re
import shutil
from pathlib import Path

import numpy as np
import pandas as pd
from numpy.ma.core import shape

from labnas.remote.imaging import ImagingNas


TEMP_DIR = Path("/home/mathis/Code/gitlab/labnas/data/temp")
CSV_TIMESTAMP_FORMATS = [
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S,%f"
]


def update_with_name(base_dict: dict, new_dict: dict, prefix: str) -> dict:
    assert isinstance(new_dict, dict)
    for key, value in new_dict.items():
        base_dict[f"{prefix}_{key}"] = value
    return base_dict

def scan_multipage_tiffs(base_directory: Path, nas: ImagingNas, limit: int | None = None) -> list:
    """Get all tifs that are in a multipage folder."""
    tifs = []
    _, mouse_candidates = nas.list_files_and_folders(base_directory)
    for single_mouse in mouse_candidates:
        _, date_candidates = nas.list_files_and_folders(single_mouse)
        for single_date in date_candidates:
            multipage = single_date / "twophoton" / "multipage_tiff"
            if nas.is_dir(multipage):
                files,  _ = nas.list_files_and_folders(multipage)
                for single_file in files:
                    if single_file.suffix == ".tif":
                        tifs.append(single_file)
                        if limit is not None:
                            if len(tifs) == limit:
                                return tifs
    tifs = _sort_by_date(tifs)
    return tifs


def _sort_by_date(tifs: list) -> np.ndarray:
    dates = [tif.parent.parent.parent.name for tif in tifs]
    i_sort = np.argsort(dates)
    tifs = np.asarray(tifs)[i_sort]
    return tifs

def find_matching_stim(tif_timestamp: datetime.datetime, tif_path: Path, nas: ImagingNas) -> Path:
    """Find stim files that correspond to recording."""
    csv_candidates = _find_matching_csvs(tif_path, nas)
    if len(csv_candidates) == 0:
        raise FileNotFoundError(f"No csv files found for {tif_path}")
    csv_files, csv_timestamps = _extract_timestamps(csv_candidates, nas)
    time_differences = []
    for single_timestamp in csv_timestamps:
        delta = tif_timestamp - single_timestamp
        time_differences.append(delta.total_seconds())
    i_min = np.argmin(np.abs(time_differences))
    print(f"\t {csv_files[i_min].parent.name}: {time_differences[i_min]:.2f} s difference to onset")
    csv_file = csv_files[i_min]
    stim_folder = csv_file.parent
    return stim_folder


def _find_matching_csvs(tif: Path, nas: ImagingNas) -> list:
    stim_folder = tif.parent.parent.parent / "stim"
    csv_files = []
    if nas.is_dir(stim_folder):
        _, folders = nas.list_files_and_folders(stim_folder)
        for single_folder in folders:
            files, _ = nas.list_files_and_folders(single_folder)
            for single_file in files:
                if single_file.name == "flip_info.csv":
                    csv_files.append(single_file)
    return csv_files


def _extract_timestamps(csv_files: list, nas: ImagingNas) -> tuple:
    """For all stimuli in the same folder as the tif, extract timestamps."""
    local_folder = Path("/home/mathis/Code/gitlab/labnas/data/temp")
    timestamps = []
    valid_files = []
    for single_csv in csv_files:
        # download
        local_copy = local_folder / single_csv.name
        if local_copy.is_file():
            os.remove(local_copy)
        nas.download_file(single_csv, local_copy)

        # extract
        df = pd.read_csv(local_copy)
        if "datetime" in df.columns:
            timestamp = _get_csv_timestamp(df)
            os.remove(local_copy)
            valid_files.append(single_csv)
            timestamps.append(timestamp)
    return valid_files, timestamps


def _get_csv_timestamp(df: pd.DataFrame) -> datetime.datetime:
    timestamp_string = df["datetime"].values[0]
    timestamp = None
    for possible_format in CSV_TIMESTAMP_FORMATS:
        try:
            timestamp = datetime.datetime.strptime(timestamp_string, possible_format)
            break
        except ValueError as ve:
            pass
    if timestamp is None:
        raise ve
    return timestamp


def check_file_name_with_list(tif_name: str, list_of_words: list[str]) -> bool:
    should_use = False
    match = None
    for candidate in list_of_words:
        if candidate in tif_name:
            should_use = True
            match = candidate
    return should_use, match


def check_file_name_for_disqualifiers(tif_name: str) -> bool:
    should_use = False
    if "pre" in tif_name:
        pass
    elif "post" in tif_name:
        pass
    elif "aborted" in tif_name:
        pass
    elif "zstack" in tif_name:
        pass
    else:
        should_use = True
    return should_use
