import os
import joblib

from pathlib import Path

import pandas as pd
import numpy as np

from sklearn.metrics.pairwise import cosine_similarity

from mlinvitrotox.constants import (
    # IDs
    CHEM_ID,
)


def get_aeids_from_path(base_path):
    """
    Get a list of AEIDs from the base_path directory.

    Parameters:
    - base_path: The base directory containing AEID directories.

    Returns:
    A list of AEIDs (as strings) found in the base_path.
    """
    # List all items in base_path
    items = os.listdir(base_path)
    # Filter items to only include directories (assuming AEIDs are directories)
    aeids = [item for item in items if os.path.isdir(Path(base_path) / item)]
    return aeids


def load_application_data(
    fps_input_file,
    id=None,
):
    if isinstance(fps_input_file, Path) and fps_input_file.suffix == ".csv":
        df = pd.read_csv(fps_input_file)
    else:
        df = pd.read_parquet(fps_input_file)

    # List of possible chemical ID columns
    possible_id_columns = ["dtxsid", "guid", "features", "sirius_id"]
    if id is not None:
        possible_id_columns += [id]

    # Initialize a variable to store the name of the found ID column
    found_id_column = None

    # Check and rename the ID column
    cols_df = [col.lower() for col in df.columns]
    for column in possible_id_columns:
        if column.lower() in cols_df:
            found_id_column = column
            df.rename(columns={column: "chem_id"}, inplace=True)
            break  # Assuming only one such column exists, exit the loop after renaming

    # If no predefined ID column is found, prompt the user for selection
    if found_id_column is None:
        print(
            "No predefined ID column found. Rerun with the option --id set to the ID column in your input file."
        )
        return df

    # Filter columns to retain only the ID column and those with numbers in their names (considered feature columns)
    feature_columns = [
        col
        for col in df.columns
        if any(char.isdigit() for char in col) or col == "chem_id"
    ]
    df = df[feature_columns]
    return df


def get_true_fingerprints_for_selected_chemicals(
    selected_chemicals_file,
    truefps_df,
    target_variable,
):
    # load selected chemicals
    chem_df = pd.read_csv(selected_chemicals_file)

    # get true fingerprints for selected chemicals
    selected_truefps_df = truefps_df[
        truefps_df[CHEM_ID].isin(chem_df[CHEM_ID])
    ].reset_index(drop=True)
    columns_to_drop = [CHEM_ID, target_variable]
    selected_truefps_df = selected_truefps_df.drop(
        columns=[col for col in columns_to_drop if col in selected_truefps_df.columns]
    )

    return selected_truefps_df


def load_preprocessing_and_classifier(
    base_path,
):
    """
    Load a single classifier based on the provided path.

    Parameters:
    - base_path: The path

    Returns:
    The loaded classifier and preprocessing pipeline.
    """
    preprocessor_path = Path(base_path) / "preprocessing_model.joblib"
    classifier_path = (
        Path(base_path) / "XGBClassifier" / "best_estimator_full_data.joblib"
    )

    try:
        preprocessing_model = joblib.load(preprocessor_path)
    except FileNotFoundError:
        preprocessing_model = None

    try:
        classifier = joblib.load(classifier_path)
    except FileNotFoundError:
        classifier = None

    return classifier, preprocessing_model


def calculate_maximum_similarity(
    preprocessed_predfps,
    preprocessed_truefps,
):
    # calculate cosine similarity for each pair of chemicals
    cos_sim_matrix = cosine_similarity(
        preprocessed_predfps,
        preprocessed_truefps,
    )
    # take the maximum similarity for each application chemical to any of the training chemicals
    max_similarities = cos_sim_matrix.max(axis=1)

    return max_similarities


def calculate_predictions(
    classifier,
    preprocessed_predfps,
    chem_ids,
    max_similarities,
    aeid,
):
    # get predictions
    predictions = classifier.predict(preprocessed_predfps)
    prediction_probs = classifier.predict_proba(preprocessed_predfps)[:, 1]

    # combine with other features
    pred_df = pd.concat(
        (
            pd.Series(chem_ids, name="chem_id"),
            pd.Series(predictions, name="prediction"),
            pd.Series(prediction_probs, name="probability"),
            pd.Series(max_similarities, name="similarity"),
        ),
        axis=1,
    )
    pred_df.insert(loc=0, column="aeid", value=aeid)

    return pred_df


def calculate_endpoint_score(predictions_df):
    # remove not annotated mechanistic targets
    filtered_predictions_df = predictions_df[
        predictions_df["MechanisticTarget"] != "not_annotated"
    ]

    # group and calculate endpoint score
    cols_gb = ["chem_id", "MechanisticTarget", "signal_direction"]
    endpoint_score = (
        filtered_predictions_df.groupby(cols_gb)["prediction"]
        .agg(lambda x: x.sum() / len(x))
        .reset_index(name="endpoint_score")
    )
    # merge with predictions data frame
    predictions_df = pd.merge(
        predictions_df,
        endpoint_score,
        on=cols_gb,
        how="left",
    )
    predictions_df["endpoint_score"] = predictions_df["endpoint_score"].fillna(np.nan)

    # calculate number of endpoints per mechanistic target
    endpoints_per_mech_target = (
        filtered_predictions_df.groupby(cols_gb[1:])["aeid"]
        .nunique()
        .reset_index(name="endpoints_count")
    )
    # merge with predictions data frame
    predictions_df = pd.merge(
        predictions_df,
        endpoints_per_mech_target,
        on=cols_gb[1:],
        how="left",
    )

    return predictions_df


def sort_by_aeid_and_chem_id(df):
    df["sort"] = df["chem_id"].str.split("_", expand=True)[0].astype("int")
    df["sort_adduct"] = df["chem_id"].str.split("_", expand=True)[3]
    df["sort_adduct"] = df["sort_adduct"].str.strip("[]+")
    df["aeid"] = df["aeid"].astype("int")
    df = df.sort_values(["sort", "sort_adduct", "aeid"], ascending=[True, True, True])
    df = df.drop(columns=["sort", "sort_adduct"])
    return df


def sort_by_column(df, col):
    df["sort"] = df[col].str.split("_", expand=True)[0].astype("int")
    df = df.sort_values(["sort", col])
    df = df.drop(columns=["sort"])
    return df
