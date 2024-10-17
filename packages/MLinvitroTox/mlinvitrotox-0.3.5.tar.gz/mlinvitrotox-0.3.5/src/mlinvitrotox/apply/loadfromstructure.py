import io
import pkgutil
from pathlib import Path

import pandas as pd

import mlinvitrotox.utils.get_true_fps as get_truefps

import click


@click.command("loadsmiles")
@click.option(
    "--input_file",
    "-i",
    help="path to csv file with two mandatory columns (id, smiles)",
    required=True,
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--id",
    "-d",
    help="column name of id",
    default="ID",
    required=True,
)
@click.option(
    "--smiles",
    "-s",
    help="column name of smiles",
    default="SMILES",
    required=True,
)
@click.option(
    "--output_file",
    "-o",
    default=None,
    help="path to csv file where the processed output should be stored. It will be created if it does not exist.",
)
def load_from_structure(input_file, id, smiles, output_file):
    """
    Calculate true SIRIUS fingerprints from SMILES

    """

    # read fingerprint definitions
    sirius_fps_data = pkgutil.get_data("mlinvitrotox", "data/csi_fingerid.tsv")
    df_csi = pd.read_csv(io.BytesIO(sirius_fps_data), sep="\t")

    # in- and output
    fps_input_path = Path(input_file)
    fps_output_path = Path(output_file)
    if not fps_output_path.parent.is_dir():
        fps_output_path.parent.mkdir(parents=True, exist_ok=True)

    # set sdf and csv output paths
    base_file_name = fps_input_path.stem
    output_dir = fps_output_path.parent.absolute()
    sdf_output_path = output_dir / f"{base_file_name}_clean.sdf"
    csv_output_path = output_dir / f"{base_file_name}_clean.csv"

    # process molecules
    get_truefps.process_molecules(
        id,
        smiles,
        fps_input_path,
        df_csi,
        fps_output_path,
        csv_output_path,
        sdf_output_path,
        store_as_csv=True,
    )


if __name__ == "__main__":
    load_from_structure()
