from typing import Iterable, Dict
from pathlib import Path


def write_ioi(result_dir: Path, name: str, data: Iterable[Iterable[str]]):
    with open(result_dir.joinpath(name + ".txt"), "w") as fh:
        for line in data:
            fh.write(", ".join(line) + "\n")


def write_doi(result_dir: Path, name: str, data: Dict[str, Iterable[str]]):
    with open(result_dir.joinpath(name + ".txt"), "w") as fh:
        for key, line in data.items():
            fh.write(key + ": " + ", ".join(line) + "\n")


def write_i(result_dir: Path, name: str, data: Iterable[str]):
    with open(result_dir.joinpath(name + ".txt"), "w") as fh:
        for line in data:
            fh.write(line + "\n")
