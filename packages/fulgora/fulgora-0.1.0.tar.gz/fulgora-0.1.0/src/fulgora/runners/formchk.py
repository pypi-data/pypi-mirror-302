import subprocess
import logging
from pathlib import Path
from fulgora.names import CHECKPOINT_NAME, FORMATTED_CHECKPOINT_NAME

jobname = "formchk"


def run(base_directory: Path):
    command = f"{jobname} {CHECKPOINT_NAME} {FORMATTED_CHECKPOINT_NAME}"

    subprocess.run(
        command, shell=True, text=True, capture_output=True, cwd=str(base_directory)
    )


def check_files(base_directory: Path):
    formatted_checkpoint_path = base_directory / FORMATTED_CHECKPOINT_NAME
    assert (
        formatted_checkpoint_path.exists()
    ), f"Log file could not be found, indicating the {jobname} didn't finish."
