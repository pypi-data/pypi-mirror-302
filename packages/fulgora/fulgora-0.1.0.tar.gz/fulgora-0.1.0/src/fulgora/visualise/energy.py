from pathlib import Path
import polars as pl
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go

import argparse


def extract_time(time_file: str) -> float | None:
    try:
        with open(time_file, "r") as file:
            content = file.read().strip()
            time_in_seconds = float(content.split(" ")[0])
            return time_in_seconds
    except Exception as e:
        return None


def extract_basis_set(name: str) -> str:
    return "-".join(name.split("_")[0].split("-")[1:])


def visualise(args):
    main_folder_path = Path(args.directory)
    energy_data = []

    for subfolder in main_folder_path.iterdir():
        if not subfolder.is_dir():
            continue

        energy_file = subfolder / "energies.csv"
        time_file = subfolder / "time.txt"

        if not energy_file.exists() or not time_file.exists():
            continue

        df = pl.read_csv(energy_file)
        if "SCF Energy" not in df.columns:
            continue

        subfolder_name = subfolder.name
        subfolder_name = extract_basis_set(subfolder_name)
        time_in_seconds = extract_time(time_file) if time_file.exists() else None

        energy_data.extend(
            [
                {
                    "Basis Set": subfolder_name,
                    "SCF Energy": energy,
                    "Time (s)": time_in_seconds,
                }
                for energy in df["SCF Energy"].to_list()
            ]
        )

    energy_df = pl.DataFrame(energy_data)
    energy_df = energy_df.sort("Time (s)")
    energy_pd_df = energy_df.to_pandas()

    if args.scatter:
        fig = px.scatter(
            energy_pd_df,
            x="Time (s)",
            y="SCF Energy",
            color="Basis Set",
            title="SCF Energy vs Time (s)",
            labels={"Time (s)": "Time (seconds)", "SCF Energy": "SCF Energy (kJ/mol)"},
        )

        fig.write_image(args.output)
    else:
        fig = make_subplots(
            rows=2,
            cols=1,
            subplot_titles=("SCF Energy per Run", "Time per Run"),
        )

        fig.add_trace(
            go.Scatter(
                x=energy_pd_df["Basis Set"],
                y=energy_pd_df["SCF Energy"],
                mode="lines+markers",
                name="SCF Energy",
                marker=dict(color="blue"),
            ),
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Bar(
                x=energy_pd_df["Basis Set"],
                y=energy_pd_df["Time (s)"],
                name="Time (s)",
                marker=dict(color="orange"),
            ),
            row=2,
            col=1,
        )

        fig.update_layout(
            height=600,
            title_text="SCF Energy and Time per Run",
            xaxis_title="Basis Set",
            yaxis_title="SCF Energy (kJ/mol)",
        )
        fig.update_yaxes(title_text="Time (s)", row=2, col=1)
        fig.write_image(args.output)


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-directory",
        help="Path to the output directory of the fulgora run",
        required=True,
    )
    parser.add_argument("-output", help="Path to the output plot", required=True)
    parser.add_argument(
        "-scatter",
        help="Path to the output plot",
        action=argparse.BooleanOptionalAction,
    )

    return parser.parse_args()


def main():
    args = parse_arguments()
    visualise(args)
