import datetime
from pathlib import Path

from labnas.remote.imaging import ImagingNas


DATE_FORMAT = "%Y%m%d"
TIME_FORMAT = "%H%M%S%f"


def get_empty_eyetracking_info() -> dict:
    info = {
        "left_timestamp": None,
        "right_timestamp": None,
    }
    return info

def find_eyetracking(tif_path: Path, nas: ImagingNas) -> Path:
    """Find eyetracking data that corresponds to TIFF."""
    base_folder = tif_path.parent.parent.parent / "eyetracking"
    if not nas.is_dir(base_folder):
        raise FileNotFoundError(f"No eyetracking folder for {tif_path}")
    _, folders = nas.list_files_and_folders(base_folder)
    folder_names = [x.name for x in folders]
    eyetracking_folder = None
    for single_folder in folders:
        if tif_path.stem == single_folder.name:
            eyetracking_folder = single_folder
            break
    if eyetracking_folder is None:
        raise FileNotFoundError(f"Cannot identify eyetracking folder among {folder_names}")
    return eyetracking_folder


def extract_eyetracking_info(eyetracking_folder: Path, nas: ImagingNas) -> dict:
    """Extract timestamps from eyetracking file names."""
    _, folders = nas.list_files_and_folders(eyetracking_folder)
    date_per_eye = {
        "right_timestamp": None,
        "left_timestamp": None,
    }
    for single_folder in folders:
        if single_folder.name in ["left_eye", "right_eye"]:
            files, _ = nas.list_files_and_folders(single_folder)
            for single_file in files:
                if single_file.suffix == ".mp4":
                    parts = single_file.stem.split("_")
                    date_string = parts[-2]
                    time_string = parts[-1]
                    dt_date = datetime.datetime.strptime(date_string, DATE_FORMAT)
                    dt_time = datetime.datetime.strptime(time_string, TIME_FORMAT)
                    dt_full = dt_time.replace(year=dt_date.year, month=dt_date.month, day=dt_date.day)
                    key = "left_timestamp" if single_folder.name == "left_eye" else "right_timestamp"
                    date_per_eye[key] = dt_full
    return date_per_eye