"""Basic local functions."""
import logging
import re
from pathlib import Path

import numpy as np


LEICA_PATTERN = r"(?<=[tz])[0-9]+(?=_ch00)"


def assert_single_stack(tif_files: list[Path]) -> str:
    """Check that there is only one stack in list of tifs"""
    tif_origin = identify_tif_origin(tif_files[0])
    if tif_origin == "leica":
        stack_names = get_leica_stack_names(tif_files)
    elif tif_origin == "basler":
        stack_names = get_basler_stack_names(tif_files)
    else:
        raise NotImplementedError(f"{tif_origin=} not implemented.")
    assert len(stack_names) == 1, f"More than 1 stack in {tif_files[0].parent}: {stack_names}"
    print(f"Only one stack: {stack_names[0]}")
    return stack_names[0]


def identify_tif_origin(tif: Path) -> str:
    """
    Identify where tif comes from.
    Relies on file name components added by recording software.
    """
    if "ch00" in tif.name:
        origin = "leica"
    elif "LUT" in tif.name:
        origin = "leica_metadata"
    elif "Basler" in tif.name:
        origin = "basler"
    else:
        raise ValueError(f"Cannot identify origin of tif {tif}")
    return origin


def get_leica_stack_names(tif_files: list[Path]) -> list:
    """Get stack names in leica tifs"""
    stack_names = []
    for file in tif_files:
        stack_name = re.findall(r".+(?=_[tz][0-9]+)", file.name)[0]
        if stack_name not in stack_names:
            stack_names.append(stack_name)
    return stack_names


def get_basler_stack_names(tif_files: list[Path]) -> list:
    stack_names = []
    for file in tif_files:
        file_name = file.name
        stack_name = re.findall(r"(?<=__)[0-9]+_[0-9]+", file_name)[0]
        if stack_name not in stack_names:
            stack_names.append(stack_name)
    return stack_names


def list_tif_files(folder: Path) -> list:
    """List all tif files in a local folder."""
    tif_files = []
    for element in folder.iterdir():
        if element.is_file():
            if element.suffix in [".tif", ".tiff"]:
                tif_files.append(element)
    return tif_files


def sort_tif_files(tif_files: list[Path], logger: logging.Logger | None = None) -> np.ndarray:
    """Sort tif files by frame index."""
    tif_origin = identify_tif_origin(tif_files[0])
    if tif_origin == "leica":
        frame_numbers = [get_leica_frame_number(x) for x in tif_files]
    elif tif_origin == "basler":
        frame_numbers = [get_basler_frame_number(x) for x in tif_files]
    else:
        raise ValueError(f"{tif_origin=} not implemented.")
    unique_frames = np.unique(frame_numbers)
    assert unique_frames.size == len(tif_files)
    message = f"{tif_origin=}"
    if logger is None:
        print(message)
    else:
        logger.info(message)
    check_completeness(frame_numbers, logger)
    sort_vector = np.argsort(frame_numbers)
    tif_files = np.asarray(tif_files)
    tif_files = tif_files[sort_vector]
    return tif_files


def get_leica_frame_number(leica_file: Path) -> int:
    """Extract frame number from leica file name"""
    frame_number = re.findall(LEICA_PATTERN, leica_file.name)[0]
    # print(leica_file.name, frame_number)
    frame_number = int(frame_number)
    return frame_number


def get_basler_frame_number(basler_file: Path) -> int:
    """Extract frame number from basler file name"""
    frame_number = re.findall(r"[0-9]+(?=.tif)", basler_file.name)[0]
    frame_number = int(frame_number)
    return frame_number


def check_completeness(frame_numbers: list, logger: logging.Logger | None = None) -> None:
    """Check that all frame numbers are present."""
    lowest = np.min(frame_numbers)
    highest = np.max(frame_numbers)
    assert lowest < highest, f"{lowest=}, {highest=}"
    all_possible = np.arange(lowest, highest)
    if not np.all(np.isin(all_possible, frame_numbers)):
        is_missing = np.logical_not(np.isin(all_possible, frame_numbers))
        missing_numbers = all_possible[is_missing]
        n_missing = np.sum(is_missing)
        n_total = all_possible.size
        fraction_missing = n_missing / n_total
        if logger is None:
            print(f"The following frame numbers are missing:")
            print(missing_numbers)
        else:
            logger.info(f"The following frame numbers are missing:")
            logger.info(missing_numbers)
        raise TifFileMissingException(f"{n_missing}/{n_total} ({fraction_missing:.2%}) frame numbers are missing")
    message = f"Frame numbers: {lowest} -> {highest} (count: {len(frame_numbers)})"
    if logger is None:
        print(message)
    else:
        logger.info(message)


class TifFileMissingException(Exception):
    pass
