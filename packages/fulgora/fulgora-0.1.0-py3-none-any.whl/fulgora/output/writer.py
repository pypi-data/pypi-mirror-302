import polars as pl
from pathlib import Path
from fulgora.names import ENERGY_CSV_NAME, TIME_NAME


def write_energy(energy: dict, base_directory: Path):
    df = pl.from_dict(energy)
    output_path = base_directory / ENERGY_CSV_NAME
    df.write_csv(output_path)


def write_duration(duration: float, base_directory: Path):
    output_path = base_directory / TIME_NAME
    with open(output_path, "w") as file:
        file.write(f"{duration} seconds")
