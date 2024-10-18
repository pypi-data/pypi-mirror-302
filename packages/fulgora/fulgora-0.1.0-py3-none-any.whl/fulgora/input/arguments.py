import dataclasses
from typing import Optional


@dataclasses.dataclass
class JobParameters:
    model: str
    cpus: Optional[int] = None
    memory: int = 16
    basis: str = "6-31G(d)"
    calculation: str = "Opt"
    name: Optional[str] = None
    charge: int = 0
    multiplicity: int = 1
    outdir: Optional[str] = None
    dev: bool = False


def parse_arguments_to_api(
    model: str,
    cpus: Optional[int] = None,
    memory: int = 16,
    basis: str = "6-31G(d)",
    calculation: str = "Opt",
    name: Optional[str] = None,
    charge: int = 0,
    multiplicity: int = 1,
    outdir: Optional[str] = None,
    dev: bool = False,
) -> JobParameters:
    return JobParameters(
        model=model,
        cpus=cpus,
        memory=memory,
        basis=basis,
        calculation=calculation,
        name=name,
        charge=charge,
        multiplicity=multiplicity,
        outdir=outdir,
        dev=dev,
    )
