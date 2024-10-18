from pathlib import Path
from datetime import datetime


def create(args) -> Path:
    output_dir = Path(args.outdir)
    if args.dev:
        return output_dir

    output_dir.mkdir(exist_ok=True, parents=True)
    time = datetime.now()

    name = Path(args.model).stem if not args.name else args.name
    run_dir = output_dir / f"{name}_{time.strftime('%d_%m_%Y-%H:%M:%S')}"

    run_dir.mkdir(exist_ok=True)
    return run_dir
