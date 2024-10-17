from tqdm import tqdm

from pathlib import Path
import click

import pandas as pd

import mlinvitrotox.utils.predict as predict

from mlinvitrotox.constants import (
    # Paths
    MODELS_RESULTS_DIR_PATH,  # 31
    FPS_OUTPUT_DIR_PATH,
    # Files
    PRED_FPS_APPLICATION,  # 16
)

from mlinvitrotox.utils.model import Model


@click.command("eval")
@click.option("--model", "-m", default="2024-08-09_20-08-13", help="name of the model")
def run_evaluation(model):
    """
    Evaluate models

    """
    model_instance = Model()
    logs_folder = Path(MODELS_RESULTS_DIR_PATH)
    run_folder = model

    model_path = Path(logs_folder / run_folder)
    model_instance.load(model_path)

    # Get predicted application fingerprints for similarity comparison
    fps_output_directory = Path(FPS_OUTPUT_DIR_PATH)
    predfps_output_file = fps_output_directory / PRED_FPS_APPLICATION
    predfps_df = predict.load_application_data(predfps_output_file)
    predfps_df.set_index("chem_id", inplace=True)

    print("Predictions")
    predictions_df = model_instance.predict(predfps_df)
    predictions_df = predictions_df.sort_values("aeid")

    metrics_dfs_list = []

    # for each aeid
    print("Loading metric files")
    aeids = model_instance.df_assay_info["aeid"].astype("str").to_list()
    for aeid in tqdm(aeids, desc="Processing AEIDs"):
        aeid_path = (
            Path(model_instance.target_variable)
            / model_instance.ml_algorithm
            / str(aeid)
        )
        preproc_path = aeid_path / "Feature_Selection_RandomForestClassifier"

        # load metrics
        metrics_path = preproc_path / "XGBClassifier" / "test" / "metrics.csv"
        metrics_path = model_instance.get_path(metrics_path)
        met_df = pd.read_csv(metrics_path)
        met_df.insert(loc=0, column="aeid", value=aeid)
        metrics_dfs_list.append(met_df)

    # concatenate metrics and predictions
    metrics_df = pd.concat(metrics_dfs_list)
    metrics_df = metrics_df.sort_values("aeid")

    # Save predictions and metrics
    output_predictions_file = logs_folder / run_folder / "modeltraining_predictions.csv"
    output_metrics_file = logs_folder / run_folder / "modeltraining_metrics.csv"

    predictions_df = predict.sort_by_aeid_and_chem_id(predictions_df)
    predictions_df.round(5).to_csv(output_predictions_file, index=False)
    metrics_df.round(5).to_csv(output_metrics_file, index=False)
    print("Predictions and metrics stored.")


if __name__ == "__main__":
    run_evaluation()
