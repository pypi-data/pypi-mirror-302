from __future__ import annotations

import os
import subprocess
from pathlib import Path
from typing import Any, Literal, overload

BIN_DIR = Path(__file__).parent / "bin"


def bin_path(bin_name: str) -> Path:
    if os.name == "nt":
        return BIN_DIR / f"{bin_name}.exe"
    return BIN_DIR / bin_name


MSMS_BIN_PATH = bin_path("msms")


@overload
def msms(
    *args: str, return_completed_process: Literal[True], **kwargs: Any
) -> subprocess.CompletedProcess[str | bytes]: ...


@overload
def msms(
    *args: str, return_completed_process: Literal[False] = ..., **kwargs: Any
) -> int: ...


@overload
def msms(
    *args: str, return_completed_process: bool = False, **kwargs: Any
) -> int | subprocess.CompletedProcess[str | bytes]: ...


def msms(
    *args: str, return_completed_process: bool = False, **kwargs: Any
) -> int | subprocess.CompletedProcess[str | bytes]:
    complete_process = subprocess.run([MSMS_BIN_PATH, *args], **kwargs)

    if return_completed_process:
        return complete_process
    return complete_process.returncode
