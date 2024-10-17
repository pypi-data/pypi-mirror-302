from datetime import datetime
from pathlib import Path
import os

import polars as pl

from labnas.remote.imaging import ImagingNas


LOCAL_TEMP = Path("/home/mathis/Code/gitlab/labnas/data/temp")


def get_empty_daq_info() -> dict:
    info = {
        "timestamp_start": None,
        "timestamp_end": None,
        "duration_min": None,
        "triggers_twophoton": None,
        "triggers_left_eye": None,
        "triggers_right_eye": None,
        "triggers_vitals": None,
    }
    return info


def find_daq_file(stim_folder: Path, nas: ImagingNas) -> Path:
    """Find data acquisition file in stim folder."""
    files, folders = nas.list_files_and_folders(stim_folder)
    daq_file = None
    for file in files:
        if (file.name == "daq.csv") or (file.name == "labjack.csv"):
            daq_file = file
            break
    return daq_file


def extract_daq_info(daq_file: Path, nas: ImagingNas) -> dict:
    local_copy = LOCAL_TEMP / daq_file.name
    if local_copy.is_file():
        os.remove(local_copy)
    nas.download_file(daq_file, local_copy)
    df = pl.read_csv(local_copy)
    os.remove(local_copy)

    triggers_twophoton = df.filter(pl.col("interval_twophoton_scanner").is_not_null()).shape[0]

    timestamp_start = df["datetime"][0]
    timestamp_end = df["datetime"][-1]
    timestamp_start = datetime.strptime(timestamp_start, "%Y-%m-%d %H:%M:%S.%f")
    timestamp_end = datetime.strptime(timestamp_end, "%Y-%m-%d %H:%M:%S.%f")
    delta = timestamp_end - timestamp_start
    duration_min = delta.total_seconds() / 60


    info = {
        "timestamp_start": timestamp_start,
        "timestamp_end": timestamp_end,
        "duration_min": duration_min,
        "triggers_twophoton" :triggers_twophoton,
    }

    # optional
    for col in ["left_eye_camera", "right_eye_camera", "vitals_monitor"]:
        if col in df.columns:
            n_triggers = df.filter(pl.col(f"interval_{col}").is_not_null()).shape[0]
        else:
            n_triggers = None
        parts = col.split("_")
        shorter = "_".join(parts[:-1])
        info[f"triggers_{shorter}"] = n_triggers
    return info
