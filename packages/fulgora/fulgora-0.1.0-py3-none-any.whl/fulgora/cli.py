import argparse
import re
from fulgora.input import convert
from fulgora.input import headers
from fulgora.input import footers
from fulgora.util import directory
from fulgora.runners import g16, formchk
from fulgora.output import parser, writer
from fulgora.names import GJF_NAME
from fulgora.basis_sets import basis_sets

from pathlib import Path
from shutil import which

assert which("g16"), "Gaussian is not loaded"


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("-model", help="Path to CIF file", required=True)
    parser.add_argument("-cpus", help="CPU cores", default=None, required=False)
    parser.add_argument("-memory", help="Memory (Gb)", default=16, required=False)
    parser.add_argument("-basis", help="Basis set", default="6-31G(d)", required=False)
    parser.add_argument(
        "-calculation", help="What to calculate", default="Opt", required=False
    )
    parser.add_argument("-name", help="Name for the job", default=None, required=False)
    parser.add_argument(
        "-charge", help="Charge of molecule (0, +1, -1)", default=0, required=False
    )
    parser.add_argument(
        "-multiplicity",
        help="Multiplicity of molecule (Number of unpaired electrons = 2S+1)",
        default=1,
        required=False,
    )

    parser.add_argument("-outdir", help="Output Directory", default=16, required=False)
    parser.add_argument("-dev", help="Dev Mode", action=argparse.BooleanOptionalAction)

    return parser.parse_args()


def create_jobfile_string(args: argparse.Namespace) -> str:
    header_string = headers.create(args)
    gjf_atoms = convert.cif_to_gjf_atoms(args.model)
    return header_string + gjf_atoms + footers.end_of_file()


def write_jobfile(jobfile: str, directory: Path):
    gjf_path = directory / GJF_NAME
    with open(gjf_path, "w") as file:
        file.write(jobfile)


def main():
    args = parse_arguments()
    if re.match(r"\d+", args.basis):
        basis_index = int(args.basis)
        if basis_index > len(basis_sets):
            raise RuntimeError("Unknown basis set number")
        args.basis = basis_sets[basis_index]
        args.name = f"{args.name}-{args.basis}"

    base_directory = directory.create(args)

    # Create job file
    jobfile_string = create_jobfile_string(args)
    write_jobfile(jobfile=jobfile_string, directory=base_directory)

    # Run Gaussian16
    duration = g16.run(base_directory)
    g16.check_files(base_directory)

    # # Convert checkpoint into formatted checkpoint
    formchk.run(base_directory)
    formchk.check_files(base_directory)

    # Parse formatted checkpoint
    energy = parser.get_energy(base_directory)
    writer.write_energy(energy, base_directory)
    writer.write_duration(duration, base_directory)
