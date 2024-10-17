import os
from pathlib import Path

import numpy as np

from labnas.remote.imaging import ImagingNas



def get_empty_suite2p_info() -> dict:
    info = {
        "rois": "unknown",
        "frames": "unknown",
    }
    return info


def extract_suite2p_info(remote_folder: Path, nas: ImagingNas, local_temp: Path) -> dict:
    path = _find_f_npy(remote_folder, nas)
    local_copy = local_temp / path.name
    if local_copy.is_file():
        os.remove(local_copy)
    nas.download_file(path, local_copy)
    cells = np.load(local_copy, allow_pickle=True)
    os.remove(local_copy)
    info = {
        "rois": cells.shape[0],
        "frames": cells.shape[1],
    }
    return info


def _find_f_npy(remote_folder: Path, nas: ImagingNas) -> Path:
    cells_file = None
    files, folders = nas.list_files_and_folders(remote_folder)
    for file in files:
        if file.name == "F.npy":
            cells_file = file
            break
    for folder in folders:
        if cells_file is None:
            subfiles, _ = nas.list_files_and_folders(folder)
            for subfile in subfiles:
                if subfile.name == "F.npy":
                    cells_file = subfile
                    break
    if cells_file is None:
        raise FileNotFoundError(f"Cannot find F.npy in {remote_folder}")
    return cells_file
