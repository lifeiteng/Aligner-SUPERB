import os
from pathlib import Path
from typing import Dict, List

from lhotse.utils import Pathlike
from praatio import textgrid


def find_files(
    root: Pathlike,
    extension: str = ".TextGrid",
) -> List[str]:
    """
    Find all files with a given extension in a directory tree.
    """
    found = []
    for path, _, files in os.walk(root):
        for file in files:
            if file.endswith(extension):
                found.append(os.path.join(path, file))
    return found


def map_files(files: List[str]) -> Dict[str, str]:
    """
    Map file stem to full path.
    """
    files_map = {}
    for file in files:
        key = Path(file).stem
        assert key not in files_map, f"Duplicate key: {key}"
        files_map[key] = file
    return files_map


def parse_textgrid(files_map: Dict[str, str]) -> Dict[str, str]:
    """
    Parse TextGrid file.
    """
    ttg = {}
    for name, file_path in files_map.items():
        ttg[name] = textgrid.openTextgrid(file_path, includeEmptyIntervals=False)
    return ttg
