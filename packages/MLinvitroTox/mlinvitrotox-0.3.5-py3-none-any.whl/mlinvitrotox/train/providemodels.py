from pathlib import Path

import click

from mlinvitrotox.utils.model import Model

from mlinvitrotox.constants import (
    # Paths
    MODELS_RESULTS_DIR_PATH,  # 31
)


@click.command("export")
@click.option(
    "--model",
    "-m",
    required=True,
    default="2024-08-09_20-08-13",
    help="name of the model",
)
@click.option(
    "--output", 
    "-o", 
    required=True, 
    help="output filename (.itox) or directory"
)
@click.option(
    "--export_stats", 
    "-s", 
    required=True, 
    default=False,
    help="include stats for app"
)
def export_model(model, output, export_stats):
    """
    Export model

    """
    model_instance = Model()
    logs_folder = Path(MODELS_RESULTS_DIR_PATH)
    model_path = Path(logs_folder / model)
    model_instance.load(model_path)
    model_instance.export(output, export_stats)


if __name__ == "__main__":
    export_model()
