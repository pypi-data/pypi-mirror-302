"""
Process frame info file.
"""

import datetime
import os

from pathlib import Path

import pandas as pd

from labnas.remote.base import SftpNas

TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def get_empty_stim_info() -> dict:
    info = {
        "timestamp_start": "unknown",
        "timestamp_end": "unknown",
        "duration_min": "unknown",
        "n_trials": "unknown",
        "n_2p_triggers": "unknown",
    }
    return info

def extract_stim_info(remote_file: Path, nas: SftpNas, local_temp: Path) -> dict:
    """Get some basics from the frame info file."""
    local_copy = local_temp / remote_file.name
    nas.download_file(remote_file, local_copy)
    assert local_copy.is_file()
    df = pd.read_csv(local_copy)
    os.remove(local_copy)

    if "flip_datetime" in df.columns:
        first_dt = df["flip_datetime"].dropna().values[0]
        first_dt = datetime.datetime.strptime(first_dt, TIMESTAMP_FORMAT)

        last_dt = df["flip_datetime"].dropna().values[-1]
        last_dt = datetime.datetime.strptime(last_dt, TIMESTAMP_FORMAT)
        elapsed = last_dt - first_dt
        elapsed = elapsed.total_seconds()
        minutes = elapsed / 60
    else:
        first_dt = last_dt = minutes = "unknown"

    if "i_twophoton_frame" in df.columns:
        n_triggers = df["i_twophoton_frame"].max() + 1
    else:
        n_triggers = None

    if "i_trial" in df.columns:
        n_trials = int(df["i_trial"].max() + 1)
    else:
        n_trials = "unknown"

    info = {
        "timestamp_start": first_dt,
        "timestamp_end": last_dt,
        "duration_min": minutes,
        "n_trials": n_trials,
        "n_2p_triggers": n_triggers,
    }
    return info


def get_timestamp(remote_file: Path, nas: SftpNas, local_temp: Path) -> datetime.datetime:
    """Get the first timestamp of a remote frame info file."""
    local_copy = local_temp / remote_file.name
    nas.download_file(remote_file, local_copy, overwrite=True)
    assert local_copy.is_file()
    df = pd.read_csv(local_copy)
    os.remove(local_copy)

    first_dt = df["datetime"].values[0]
    first_dt = datetime.datetime.strptime(first_dt, TIMESTAMP_FORMAT)
    return first_dt