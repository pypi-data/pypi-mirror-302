from pathlib import Path
from fulgora.names import FORMATTED_CHECKPOINT_NAME
from fulgora.util.units import convert_hartree_to_kjmol

import re


def extract_energy(line: str) -> tuple:
    # Use regex to find the first word and the last number
    match = re.search(r"(\S+ \S+).*?([-+]?\d*\.\d+E[+-]?\d+)", line)
    if match:
        name = match.group(1)  # First name (SCF Energy)
        value = float(match.group(2))  # Last number, converted to float
        return (name, value)
    else:
        return None  # Return None if the pattern is not found


def get_energy(base_directory: Path) -> dict:
    energies = {}

    with open(base_directory / FORMATTED_CHECKPOINT_NAME, "r") as file:
        for line in file:
            if line.find("Energy") == -1:
                continue
            if "R" not in line:
                continue

            line = line.removesuffix("\n")

            name, energy_hartree = extract_energy(line)
            energy_kjmol = convert_hartree_to_kjmol(energy_hartree)
            energies[name] = energy_kjmol

    return energies
