import sys

from pathlib import Path

import mlinvitrotox.utils.get_predicted_fps as get_predfps
import mlinvitrotox.utils.predict as predict

from mlinvitrotox.constants import (
    # Files
    SIRIUS_FPS_DEFINITIONS,
)

import click


@click.command("load")
@click.option(
    "--sirius_input_folder",
    "-i",
    help="path to SIRIUS files",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--output_file",
    "-o",
    default=None,
    help="path to csv file where the processed output should be stored. It will be created if it does not exist.",
)
@click.option(
    "--max_workers",
    "-w",
    default=None,
    type=int,
    help="Number of workers/process to use for loading the data",
)
def load_user_data(sirius_input_folder, output_file, max_workers=None):
    """
    Load SIRIUS data to get predicted SIRIUS fingerprints

    """
    # input path for SIRIUS files
    print("SIRIUS input folder with .fpt files:", sirius_input_folder)

    # check SIRIUS version
    matching_sirius_version = get_predfps.check_sirius_version(
        sirius_input_folder / SIRIUS_FPS_DEFINITIONS,
    )
    if not matching_sirius_version:
        "Error: This data cannot be processed."
        sys.exit()

    # read SIRIUS .fpt files
    df_fps = get_predfps.read_fps_files(
        sirius_input_folder,
        sirius_input_folder / SIRIUS_FPS_DEFINITIONS,
        threshold=0.5,
        max_workers=max_workers,
    )

    # sort and reset index
    df_fps = df_fps.sort_index().reset_index(drop=True)
    print(f"Final {sirius_input_folder.name} dataframe: {df_fps.shape[0]} entries")

    # set output file path
    if output_file is None:
        output_file = (
            Path("./results") / sirius_input_folder.name / "sirius-pred-fps.csv"
        )
    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # store output
    print(f"Writing to file {output_file}")
    if "features" in df_fps.columns:
        df_fps = predict.sort_by_column(df_fps, "features")
    df_fps.to_csv(output_file, index=False)


if __name__ == "__main__":
    load_user_data()
