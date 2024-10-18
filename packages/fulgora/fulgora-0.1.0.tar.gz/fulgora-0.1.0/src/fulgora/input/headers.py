import multiprocessing
from pathlib import Path
from fulgora.util.string import trailing_newline, leading_newline, trailing_space
from fulgora.names import CHECKPOINT_NAME


@trailing_newline
def get_nproc_shared(cpu_count: int) -> str:
    cpu_count = cpu_count if cpu_count else multiprocessing.cpu_count()
    return f"%NProcShared={cpu_count}"


@trailing_newline
def get_memory(memory: str | float) -> str:
    if isinstance(memory, float):
        return f"%mem={memory}GB"
    if isinstance(memory, str):
        memory = memory.lower()
        if memory.rfind("gb") == len(memory) - 2:
            return f"%mem={memory.rstrip('gb')}GB"

    raise RuntimeError("Could not create memory header")


@trailing_newline
def get_checkpoint():
    return f"%Chk={CHECKPOINT_NAME}"


@trailing_newline
def get_strategy(basis: str, calculation: str):
    return f"#p B3LYP/{basis} {calculation}"


@leading_newline
@trailing_newline
@trailing_newline
def get_name(args):
    name = args.name
    if not name:
        name = f"Energy calculation for {Path(args.model).stem}"
    return f" {name}"


@trailing_space
def get_charge(charge: float | str):
    return f"{charge}"


@trailing_newline
def get_multiplicity(multiplicity: float | str):
    return f"{multiplicity}"


def create(args):
    header_string = ""

    header_string += get_nproc_shared(args.cpus)
    header_string += get_memory(args.memory)
    header_string += get_checkpoint()
    header_string += get_strategy(args.basis, args.calculation)
    header_string += get_name(args)
    header_string += get_charge(args.charge)
    header_string += get_multiplicity(args.multiplicity)
    return header_string
