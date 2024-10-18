import argparse
from fulgora.input import convert, headers, footers, arguments
from fulgora.util import directory
from fulgora.runners import g16, formchk
from fulgora.output import parser, writer
from fulgora.names import GJF_NAME

from pathlib import Path
from shutil import which

assert which("g16"), "Gaussian is not loaded"


if __name__ == "__main__":
    job_params = arguments.JobParameters(
        model="path/to/cif/file.cif",
        cpus=4,
        memory=16,
        basis="6-31G(d)",
        calculation="Opt",
        name="my_job",
        charge=0,
        multiplicity=1,
        outdir="/path/to/output",
        dev=False,
    )

    print(job_params)


def create_jobfile_string(args: argparse.Namespace) -> str:
    header_string = headers.create(args)
    gjf_atoms = convert.cif_to_gjf_atoms(args.model)
    return header_string + gjf_atoms + footers.end_of_file()


def write_jobfile(jobfile: str, directory: Path):
    gjf_path = directory / GJF_NAME
    with open(gjf_path, "w") as file:
        file.write(jobfile)

    return Path(gjf_path)


def main():
    args = parse_arguments()

    base_directory = directory.create(args)

    # Create job file
    jobfile_string = create_jobfile_string(args)
    gjf_path = write_jobfile(jobfile=jobfile_string, directory=base_directory)

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
