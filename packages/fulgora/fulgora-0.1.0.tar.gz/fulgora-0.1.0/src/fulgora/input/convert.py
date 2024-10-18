import gemmi
from pathlib import Path
from typing import List
from types import SimpleNamespace


def format_coord(coordinate: float | str):
    coordinate = float(coordinate)
    return f"{coordinate:9.6f}"


def cif_to_xyz(cif_path: str | Path) -> List[dict]:
    document = gemmi.cif.read(str(cif_path))
    block = document.sole_block()
    chemcomp_atoms = block.find(
        "_chem_comp_atom.",
        [
            "type_symbol",
            "pdbx_model_Cartn_x_ideal",
            "pdbx_model_Cartn_y_ideal",
            "pdbx_model_Cartn_z_ideal",
        ],
    )
    xyz = []
    for atom in chemcomp_atoms:
        x = format_coord(atom[1])
        y = format_coord(atom[2])
        z = format_coord(atom[3])
        data = SimpleNamespace(**{"element": atom[0], "x": x, "y": y, "z": z})
        xyz.append(data)

    return xyz


def xyz_to_gjf_atoms(xyz: List[dict]) -> str:
    return_string = ""

    for atom in xyz:
        return_string += f"{atom.element}     {atom.x}   {atom.y}   {atom.z}\n"

    return return_string


def cif_to_gjf_atoms(cif_path: str | Path) -> str:
    xyz = cif_to_xyz(cif_path=cif_path)
    return xyz_to_gjf_atoms(xyz=xyz)
