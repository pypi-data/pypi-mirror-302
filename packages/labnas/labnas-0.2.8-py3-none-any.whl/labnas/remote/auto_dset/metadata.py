"""Process TIFF metadata created by Leica recording software"""
import datetime
import re
import os
from pathlib import Path

from labnas.remote.imaging import ImagingNas

DATE_PATTERN = "[0-9]{4}-[0-9]{2}-[0-9]{2}"
TIMESTAMP_PATTERN = "[0-9]+:[0-9]+:[0-9]+ [A,P]M"
TIMESTAMP_FORMAT = "%I:%M:%S %p"
FRAME_PATTERN = "(?<=FrameCount>)[0-9]+"

def find_metadata_file(tif_file: Path, nas: ImagingNas) -> Path:
    """For a tiff, find the corresponding metadata file."""
    multipage_folder = tif_file.parent
    assert multipage_folder.name == "multipage_tiff"
    metadata_folder = multipage_folder.parent / "MetaData"
    if not nas.is_dir(metadata_folder):
        raise FileNotFoundError(f"{metadata_folder}")
    meta_file = metadata_folder / f"{tif_file.stem}_Properties.xml"
    if not nas.is_file(meta_file):
        raise FileNotFoundError(f"{meta_file} does not exist")
    return meta_file

def extract_metadata_info(meta_file: Path, nas: ImagingNas, temp_local: Path) -> dict:
    """Get the timestamp of the beginning of the recording of the tiff from its metadata."""
    # download meta file
    local_copy = temp_local / meta_file.name
    if local_copy.is_file():
        os.remove(local_copy)
    nas.download_file(meta_file, local_copy)

    # get timestamp
    with open(local_copy, mode="r") as open_file:
        text = open_file.readlines()
        text = "\n".join(text)
    os.remove(local_copy)
    first, last, duration = _extract_datetime_info(text)
    n_frames = extract_frame_number(text)
    info = {
        "frames": n_frames,
        "timestamp_start": first,
        "timestamp_end": last,
        "duration_min": duration,
    }
    return info

def get_empty_metadata_info() -> dict:
    metadata_info = {
        "frames": "unknown",
        "timestamp_start": "unknown",
        "timestamp_end": "unknown",
        "duration_min": "unknown",
    }
    return metadata_info

def _extract_datetime_info(text: str) -> tuple:
    dates = re.findall(DATE_PATTERN, text)
    timestamps = re.findall(TIMESTAMP_PATTERN, text)

    # first frame
    first_date = dates[0]
    first_time = timestamps[0]
    dt_first = _convert_to_dt(first_date, first_time)

    # last frame
    last_date = dates[-1]
    last_time = timestamps[-1]
    dt_last = _convert_to_dt(last_date, last_time)

    # delta
    delta = dt_last - dt_first
    duration_minutes = delta.total_seconds() / 60
    return dt_first, dt_last, duration_minutes


def _convert_to_dt(date_string: str, time_string: str) -> datetime.datetime:
    dt_date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    dt_time = datetime.datetime.strptime(time_string, TIMESTAMP_FORMAT)
    dt_full = dt_time.replace(year=dt_date.year, month=dt_date.month, day=dt_date.day)
    return dt_full


def extract_frame_number(text: str) -> int:
    number = re.findall(FRAME_PATTERN, text)[0]
    number = int(number)
    return number
