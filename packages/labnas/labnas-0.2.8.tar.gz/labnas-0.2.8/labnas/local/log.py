import datetime
import logging
import os
import sys
from pathlib import Path

from labnas.local.files import get_path_to_base

def print_to_file(file_path: Path, message: str) -> None:
    with open(file_path, mode="a") as file:
        file.write(f"{message} \n")

def get_log_path(base_path: Path | None = None) -> Path:
    if base_path is None:
        base_path = get_path_to_base() / "results" / "log"
    if not base_path.is_dir():
        os.makedirs(base_path)
    dt = datetime.datetime.now()
    dt = dt.strftime("%Y%m%d%H%M%S")
    log_file = base_path / f"{dt}.log"
    return log_file


def get_file_logger(file_path: Path) -> logging.Logger:
    logger = logging.getLogger("labnas")
    logger.setLevel(logging.DEBUG)
    stream_handler = logging.StreamHandler(stream=sys.stdout)
    file_handler = logging.FileHandler(file_path)
    formatter = logging.Formatter()
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    logger.addHandler(stream_handler)
    return logger
