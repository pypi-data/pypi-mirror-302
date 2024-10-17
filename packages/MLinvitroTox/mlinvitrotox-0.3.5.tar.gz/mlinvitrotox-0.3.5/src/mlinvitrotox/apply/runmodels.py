from pathlib import Path

import click

import mlinvitrotox.utils.predict as predict
from mlinvitrotox.utils.model import Model


@click.command("run")
@click.option(
    "--model", 
    "-m", 
    required=True, 
    default="mlinvitrotox_model.itox",
    help="name of the model or path to model file"
)
@click.option(
    "--input_file",
    "-i",
    help="input file",
    required=True,
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--id",
    "-d",
    help="column name of id",
    default=None,
    required=False,
)
@click.option(
    "--output_folder",
    "-o",
    required=True,
    type=click.Path(path_type=Path),
    help="path to directory where the processed output should be stored. It will be created if it does not exist.",
)
def run_models(input_file, model, id, output_folder):
    """
    Run models on molecular fingerprints

    """
    model_instance = Model()
    model_path = Path(model)
    model_instance.load(model_path)

    # load predicted fingerprints and get chemical ids
    df_predfps = predict.load_application_data(input_file, id)
    df_predfps.set_index("chem_id", inplace=True)

    # collect predictions for each aeid
    df_predictions = model_instance.predict(df_predfps)

    # save predictions
    output_predictions_file = output_folder / f"{model_path.stem}_predictions.csv"
    try:
        df_predictions = predict.sort_by_aeid_and_chem_id(df_predictions)
    except:
        print("The predictions dataframe was not sorted.")
    df_predictions.round(5).to_csv(output_predictions_file, index=False)
    print(f"Predictions stored to {output_predictions_file}")

    # copy metrics file from model to output folder
    output_metrics_file = output_folder / "modeltraining_metrics.csv"
    model_instance.df_metrics.to_csv(output_metrics_file, index=False)
    print(f"Model training metrics copied to {output_metrics_file}")


if __name__ == "__main__":
    run_models()
