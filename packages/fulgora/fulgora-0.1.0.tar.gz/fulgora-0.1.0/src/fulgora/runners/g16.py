import subprocess
import logging
from pathlib import Path
from fulgora.names import LOG_NAME, CHECKPOINT_NAME, GJF_NAME
import time

jobname = "g16"


def run(base_directory: Path) -> float:
    command = f"{jobname} < {GJF_NAME} > {LOG_NAME}"

    start_time = time.perf_counter()
    subprocess.run(
        command, shell=True, text=True, capture_output=True, cwd=str(base_directory)
    )
    end_time = time.perf_counter()
    duration = end_time - start_time
    return duration


def check_files(base_directory: Path):
    log_path = base_directory / LOG_NAME
    assert (
        log_path.exists()
    ), f"Log file could not be found, indicating {jobname} didn't start."

    checkpoint_path = base_directory / CHECKPOINT_NAME
    assert (
        checkpoint_path.exists()
    ), f"Checkpoint file could not be found, indicating {jobname} job didn't finish."
