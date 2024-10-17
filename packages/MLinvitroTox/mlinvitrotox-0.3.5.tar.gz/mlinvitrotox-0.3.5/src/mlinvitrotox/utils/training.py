import os
import sys
import re
import shutil

from pathlib import Path

import logging
from datetime import datetime
import joblib
import yaml
from tqdm import tqdm

import numpy as np
import pandas as pd

import matplotlib
from matplotlib import pyplot as plt

from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, TransformerMixin
from xgboost import XGBClassifier  # needed for build_pipeline()
# from sklearn.linear_model import LogisticRegression
# from sklearn.svm import SVC
# from sklearn.neural_network import MLPClassifier
# from sklearn.ensemble import RandomForestClassifier

from mlinvitrotox.constants import (
    # IDs
    CHEM_ID,
)

# Plotting backend
matplotlib.use("Agg")

LOGGER = logging.getLogger(__name__)


def empty_pytcpl_input_directory(
    pytcpl_input_folder,
):
    for filename in os.listdir(pytcpl_input_folder):
        file_path = Path(pytcpl_input_folder) / filename
        if os.path.isfile(file_path):
            os.unlink(file_path)
        elif os.path.isdir(file_path):
            shutil.rmtree(file_path)


def copy_pytcpl_parquet_files(
    remote_pytcpl_folder,
    pytcpl_input_folder,
):
    for filename in os.listdir(remote_pytcpl_folder):
        if filename.endswith(".parquet.gzip"):
            parquet_path = Path(remote_pytcpl_folder) / filename
            shutil.copy2(parquet_path, pytcpl_input_folder)
            print(f"Copied {parquet_path} to {pytcpl_input_folder}")


def load_config(config_path, logs_folder):
    global START_TIME, LOG_PATH

    config = load_simple_config(config_path)

    START_TIME = datetime.now()
    LOGGER, RUN_FOLDER = init_logger(logs_folder)
    log_config_path = Path(LOG_PATH) / "log/config.yaml"
    with open(log_config_path, "w") as file:
        yaml.dump(config, file)
        LOGGER.info(f"Config file dumped to '{log_config_path}'")

    return config, START_TIME, LOGGER, RUN_FOLDER, LOG_PATH


def load_simple_config(config_path):
    with open(config_path, "r") as file:
        config = yaml.safe_load(file)
        if config["ignore_warnings"]:
            import warnings

            warnings.filterwarnings("ignore")

    return config


def init_target_variable(target_variable):
    global TARGET_VARIABLE, DUMP_FOLDER
    TARGET_VARIABLE = target_variable
    DUMP_FOLDER = os.path.join(str(LOG_PATH), str(TARGET_VARIABLE))
    os.makedirs(DUMP_FOLDER, exist_ok=True)
    return TARGET_VARIABLE


def init_ml_algo(ml_algorithm, config_models_path):
    global ML_ALGORITHM, DUMP_FOLDER
    ML_ALGORITHM = ml_algorithm

    # load config models file
    with open(config_models_path, "r") as file:
        config_estimators = yaml.safe_load(file)

    # store config models file in log folder
    config_models_file = config_models_path.split("/")[-1]
    with open(os.path.join(LOGGER_FOLDER, config_models_file), "w") as file:
        yaml.dump(config_estimators, file)

    # create dump folder
    DUMP_FOLDER = os.path.join(LOG_PATH, TARGET_VARIABLE, str(ml_algorithm))
    os.makedirs(DUMP_FOLDER, exist_ok=True)

    return config_estimators


def init_aeid(aeid):
    global AEID, DUMP_FOLDER
    AEID = str(aeid)
    DUMP_FOLDER = os.path.join(
        str(LOG_PATH), str(TARGET_VARIABLE), str(ML_ALGORITHM), str(AEID)
    )
    os.makedirs(DUMP_FOLDER, exist_ok=True)


def init_preprocessing_pipeline(preprocessing_pipeline):
    global PREPROCESSING_PIPELINE, DUMP_FOLDER
    preprocessing_pipeline_name = preprocessing_pipeline[
        -1
    ].estimator.__class__.__name__
    PREPROCESSING_PIPELINE = f"Feature_Selection_{preprocessing_pipeline_name}"
    LOGGER.info(f"Apply {PREPROCESSING_PIPELINE}..")
    DUMP_FOLDER = os.path.join(
        str(LOG_PATH),
        str(TARGET_VARIABLE),
        str(ML_ALGORITHM),
        str(AEID),
        str(PREPROCESSING_PIPELINE),
    )
    os.makedirs(DUMP_FOLDER, exist_ok=True)
    return PREPROCESSING_PIPELINE


def init_estimator_pipeline(estimator_name):
    global ESTIMATOR_PIPELINE, DUMP_FOLDER
    ESTIMATOR_PIPELINE = estimator_name
    DUMP_FOLDER = os.path.join(
        str(LOG_PATH),
        str(TARGET_VARIABLE),
        str(ML_ALGORITHM),
        str(AEID),
        str(PREPROCESSING_PIPELINE),
        str(ESTIMATOR_PIPELINE),
    )
    os.makedirs(DUMP_FOLDER, exist_ok=True)
    return ESTIMATOR_PIPELINE


def init_validation_set(validation_set):
    global VALIDATION_SET, DUMP_FOLDER
    VALIDATION_SET = validation_set
    LOGGER.info(f"Validation Set: {VALIDATION_SET}")
    DUMP_FOLDER = os.path.join(
        str(LOG_PATH),
        str(TARGET_VARIABLE),
        str(ML_ALGORITHM),
        str(AEID),
        str(PREPROCESSING_PIPELINE),
        str(ESTIMATOR_PIPELINE),
        str(VALIDATION_SET),
    )
    os.makedirs(DUMP_FOLDER, exist_ok=True)
    return VALIDATION_SET


def merge_assay_info(pytcpl_df, ice_df):
    """
    Adapt the assay_info DataFrame:
    - Convert aeid to string
    - Keep only specified columns
    - Left join with ice_df on aeid to exclude "Cell Viability" from "MechanisticTarget" and include unique "MechanisticTarget"
    """
    col_mt = "MechanisticTarget"

    # prepare
    pytcpl_df["aeid"] = pytcpl_df["aeid"].astype(str)
    ice_df["aeid"] = ice_df["aeid"].astype(str)

    # remove cell viability entries
    ice_df = ice_df[ice_df[col_mt] != "Cell Viability"].copy()
    # remove weird characters
    pattern = re.compile(r"\s+")
    ice_df[col_mt] = ice_df[col_mt].apply(lambda x: re.sub(pattern, " ", str(x)))
    # remove CardioTox
    ice_df["MechanisticTarget"] = ice_df["MechanisticTarget"].str.replace(
        "CardioTox_", ""
    )
    # unify not annotated
    ice_df[col_mt] = ice_df[col_mt].replace(
        ["Not Annotated", "Unspecified", "Unassigned", "nan"], "not_annotated"
    )
    # remove duplicates
    ice_df_unique = ice_df.drop_duplicates(subset=["aeid", col_mt])

    # merge
    merged_df = pd.merge(
        pytcpl_df, ice_df_unique[["aeid", col_mt]], on="aeid", how="left"
    )
    columns_to_keep = [
        "aeid",
        "assay_component_endpoint_name",
        col_mt,
        "signal_direction",
    ]
    merged_df = merged_df[columns_to_keep]
    merged_df[col_mt] = merged_df[col_mt].fillna("not_annotated")

    return merged_df


def get_aeid_files(
    pytcpl_input_folder,
    target_variable,
    assay_info_df,
):
    col_mt = "MechanisticTarget"

    # get list of pytcpl files
    parquet_files = [
        f for f in os.listdir(pytcpl_input_folder) if f.endswith(".parquet.gzip")
    ]

    # initialize
    aeid_list = []

    for filename in tqdm(parquet_files, desc="Processing aeid files"):
        file_path = Path(pytcpl_input_folder) / filename
        df = pd.read_parquet(file_path)
        if target_variable not in df.columns:
            print(f"Target variable not in {filename}")
            continue

        aeid = filename.split(".")[0]
        aeid_list.append(aeid)

    # concatenate
    aeid_df = pd.DataFrame(aeid_list, columns=["aeid"])

    # merged with aeid info to add mechanistic target
    merged_df = pd.merge(
        aeid_df,
        assay_info_df,
        on="aeid",
        how="left",
    )
    merged_df[col_mt] = merged_df[col_mt].fillna("not_annotated")
    merged_df["aeid"] = merged_df["aeid"].astype("int")

    return merged_df


def select_aeids_for_training(
    pytcpl_input_folder,
    assay_info_df,
    aeids=None,
    mech_target=None,
):
    # all aeids from pytcpl
    available_aeids = [
        f.split(".")[0]
        for f in os.listdir(pytcpl_input_folder)
        if f.endswith(".parquet.gzip")
    ]

    # select all
    if aeids is None and mech_target is None:
        selected_aeids = available_aeids

    # select from list
    if aeids is not None:
        provided_aeids = [
            str(aeid) for aeid in (aeids if isinstance(aeids, list) else [aeids])
        ]
        selected_aeids = [aeid for aeid in provided_aeids if aeid in available_aeids]
    else:
        selected_aeids = []

    # select from mechanistic target
    if mech_target is not None:
        target_pattern = mech_target.lower()
        matched_targets = assay_info_df["MechanisticTarget"].str.contains(
            target_pattern, case=False, na=False
        )
        matched_aeids = assay_info_df[matched_targets]["aeid"].astype(str).tolist()

        if len(selected_aeids) > 0:
            selected_aeids = [aeid for aeid in matched_aeids if aeid in selected_aeids]

        else:
            selected_aeids = [aeid for aeid in matched_aeids if aeid in available_aeids]

    selected_aeids = sorted(set(selected_aeids))
    return selected_aeids


def get_fingerprint_df(fps_input_file):
    if isinstance(fps_input_file, Path) and fps_input_file.suffix == ".csv":
        fps_df = pd.read_csv(fps_input_file)
    else:
        fps_df = pd.read_parquet(fps_input_file)

    integer_columns = [col for col in fps_df.columns if col.isdigit()]
    fps_df[integer_columns] = fps_df[integer_columns].astype(int)

    columns_to_keep = [col for col in fps_df.columns if col.isdigit() or col == CHEM_ID]
    fps_df = fps_df[columns_to_keep]

    print(
        f"Dataframe with true fingerprints: {fps_df.shape[0]} chemicals, {fps_df.iloc[:, 1:].shape[1]} fingerprint bits"
    )

    return fps_df


def process_single_aeid(
    pytcpl_input_folder,
    aeid,
    target_variable,
    ice_omit_filtering,
    activity_threshold,
):
    # load file
    file_path = Path(pytcpl_input_folder) / f"{aeid}.parquet.gzip"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return None
    df = pd.read_parquet(file_path)

    # apply ice omit filtering
    # (entries with NA are to be kept)
    if ice_omit_filtering:
        keep_compound_mask = df["omit_flag"].isin(["None", np.nan])
        df_kept = df[keep_compound_mask]
        num_rows_kept = len(df_kept)
        num_rows_removed = len(df) - num_rows_kept
        print(f"ICE filtering: Number of compounds kept: {num_rows_kept}")
        print(f"ICE filtering: Number of compounds removed: {num_rows_removed}")
    else:
        df_kept = df.copy()

    # get first DSSTOX column
    dsstox_cols = df_kept.columns[df_kept.columns.str.contains("dsstox")]
    if not dsstox_cols.empty:
        dsstox_col = dsstox_cols[0]
    else:
        print("No 'dsstox' column found")
        return None

    # check for target_variable
    if target_variable not in df_kept.columns:
        print(f"'{target_variable}' column not found")
        return None

    # only keep dsstox and target variable columns
    df_selected = df_kept.loc[:, [dsstox_col, target_variable]]
    df_selected.dropna(inplace=True)

    # apply activity threshold
    df_selected.loc[:, target_variable] = (
        df_selected[target_variable] >= activity_threshold
    ).astype(int)

    # merge entries for duplicate dsstox entries
    # TODO do we have duplicate dsstox entries?
    n_before = df_selected.shape[0]
    print(f"Before grouping by dsstox_col: Number of rows: {n_before}")
    df_selected = df_selected.groupby(dsstox_col).max().reset_index()
    n_after = df_selected.shape[0]
    print(f"After grouping by dsstox_col: Number of rows: {n_after}")
    if n_after != n_before:
        print("Chemicals merged through groupby by dsstox_col")

    # rename DSSTOX column
    df_selected = df_selected.rename(columns={dsstox_col: CHEM_ID})
    return df_selected


def merge_assay_and_fingerprint_df(assay_df, fps_df, selected_chemicals_file=None):
    assert CHEM_ID in assay_df.columns, f"No '{CHEM_ID}' column found in assay_df"
    assert CHEM_ID in fps_df.columns, f"No '{CHEM_ID}' column found in fps_df"
    merged_df = pd.merge(
        assay_df,
        fps_df,
        left_on=CHEM_ID,
        right_on=CHEM_ID,
        how="inner",
    ).reset_index(drop=True)
    assert (
        merged_df.shape[0] == merged_df[CHEM_ID].nunique()
    ), "Merging resulted in duplicate rows"

    if selected_chemicals_file is not None:
        merged_df[CHEM_ID].to_csv(
            Path(DUMP_FOLDER) / selected_chemicals_file, index=False
        )
    return merged_df


def cluster_threshold_all(
    df,
    n_clusters,
    random_state,
):
    from sklearn.cluster import KMeans

    # np.random.seed(random_state)
    if df.index.name != CHEM_ID:
        df = df.set_index(CHEM_ID)

    if "Cluster" in df.columns:
        clustering_features = df.drop(columns=["Cluster"]).copy()
    else:
        clustering_features = df.copy()
    kmeans = KMeans(n_clusters=n_clusters, random_state=random_state).fit(
        clustering_features
    )
    df["Cluster"] = kmeans.labels_
    return df.reset_index()


def clustering(
    df,
    target_variable,
    n_cls_0,
    n_cls_1,
    random_state,
):
    clusters_0 = []
    clusters_1 = []

    df_0 = df[df[target_variable] == 0]
    df_1 = df[df[target_variable] == 1]

    n_clusters_0 = len(df_0) // n_cls_0 + (1 if len(df_0) % n_cls_0 != 0 else 0)
    n_clusters_1 = len(df_1) // n_cls_1 + (1 if len(df_1) % n_cls_1 != 0 else 0)

    features_0 = df_0.drop(target_variable, axis=1)
    features_1 = df_1.drop(target_variable, axis=1)

    if not features_0.empty:
        df_0 = cluster_threshold_all(features_0, n_clusters_0, random_state)
        df_0[target_variable] = 0
        clusters_0.append(df_0)

    if not features_1.empty:
        df_1 = cluster_threshold_all(features_1, n_clusters_1, random_state)
        df_1[target_variable] = 1
        clusters_1.append(df_1)

    combined_df = pd.concat(clusters_0 + clusters_1, ignore_index=True)
    combined_df["Cluster_str"] = combined_df["Cluster"].astype(str)
    combined_df["target_str"] = combined_df[target_variable].astype(str)
    combined_df["clustering_rule"] = (
        combined_df["Cluster_str"] + "-" + combined_df["target_str"]
    )
    combined_df.drop(columns=["Cluster", "target_str"], inplace=True)
    return combined_df


def filter_with_sirius_quality_indexes(
    df,
    indexes_path,
    target_variable,
):
    # load selected indexes
    indexes_df = pd.read_csv(indexes_path)
    col_name = indexes_df.columns[0]
    indexes_df = indexes_df.sort_values(col_name).drop_duplicates()

    # convert to string with 4 characters
    if indexes_df["absoluteIndex"].dtype == np.int64:
        filter_indexes = indexes_df["absoluteIndex"].tolist()
    else:
        filter_indexes = indexes_df["absoluteIndex"].astype(str).tolist()
    filter_columns = [str(index).zfill(4) for index in filter_indexes]

    # add other entries and filter
    filter_columns = filter_columns + [CHEM_ID, target_variable, "clustering_rule"]
    filtered_df = df[filter_columns].copy()

    return filtered_df


def split_training_validation_data(
    filtered_df,
    pred_fps_df,
    target_variable,
):
    # get DTXSID in both data frames --> validation
    filtered_df_dtxsid = filtered_df[[CHEM_ID]]
    pred_fps_df_dtxsid = pred_fps_df[[CHEM_ID]]
    dtxsid_val = set(filtered_df_dtxsid[CHEM_ID]).intersection(
        set(pred_fps_df_dtxsid[CHEM_ID])
    )
    # get DTXSIDs not shared in data frames --> training and test
    dtxsis_train_test = set(filtered_df_dtxsid[CHEM_ID]).difference(
        set(pred_fps_df_dtxsid[CHEM_ID])
    )
    df_validation_true = filtered_df[filtered_df[CHEM_ID].isin(dtxsid_val)]
    df_validation_pred = pred_fps_df[pred_fps_df[CHEM_ID].isin(dtxsid_val)]
    df_train_test = filtered_df[filtered_df[CHEM_ID].isin(dtxsis_train_test)]
    print(f"df_validation_true {df_validation_true.shape}")
    print(f"df_validation_pred {df_validation_pred.shape}")
    print(f"df_train_test {df_train_test.shape}")
    print(f"df_train_test columns {df_train_test.columns}")

    # only keep common columns for predicted validation data frame
    common_columns = df_validation_pred.columns.intersection(df_validation_true.columns)
    df_validation_pred = df_validation_pred.loc[:, common_columns]

    # perform checks
    columns_training_test = set(
        col
        for col in df_train_test.columns
        if col != target_variable and "cluster" not in col.lower()
    )
    columns_validation_pred = set(
        col
        for col in df_validation_pred.columns
        if col != target_variable and "cluster" not in col.lower()
    )
    columns_validation_true = set(
        col
        for col in df_validation_true.columns
        if col != target_variable and "cluster" not in col.lower()
    )

    different_columns = {
        "Training/Test vs. Validation Pred": columns_training_test.symmetric_difference(
            columns_validation_pred
        ),
        "Training/Test vs. Validation True": columns_training_test.symmetric_difference(
            columns_validation_true
        ),
        "Validation Pred vs. Validation True": columns_validation_pred.symmetric_difference(
            columns_validation_true
        ),
    }

    if all(len(diff) == 0 for diff in different_columns.values()):
        print("All DataFrames have exactly the same columns (except target_variable).")
    else:
        print("DataFrames do not have the same columns (except target_variable).")
        for key, diff in different_columns.items():
            if len(diff) > 0:
                print(f"Differences in columns between {key}: {', '.join(diff)}")

    duplicates_true_exist = df_validation_true[CHEM_ID].duplicated().any()
    print(f"DTXSID duplicates in df_validation_true: {duplicates_true_exist}")
    duplicates_pred_exist = df_validation_pred[CHEM_ID].duplicated().any()
    print(f"DTXSID duplicates in df_validation_pred: {duplicates_pred_exist}")
    return df_train_test, df_validation_true, df_validation_pred


def partition_training_data(
    df_train_test,
    target_variable,
):
    # get feature_names
    feature_names = [
        col for col in df_train_test.columns if col.isdigit() and col != CHEM_ID
    ]

    # set DTXSID as index
    if CHEM_ID in df_train_test.columns:
        df_train_test = df_train_test.set_index(CHEM_ID).sort_index()

    # get X, y, and clustering rule for stratification
    X = df_train_test[feature_names]
    y = df_train_test[target_variable]  # .astype(np.uint8)
    cluster = df_train_test["clustering_rule"]

    return X, y, cluster, feature_names


def partition_validation_data(
    df_validation_true,
    df_validation_pred,
    target_variable,
    feature_names,
):
    # set DTXSID as index
    if CHEM_ID in df_validation_true.columns:
        df_validation_true = df_validation_true.set_index(CHEM_ID).sort_index()
    if CHEM_ID in df_validation_pred.columns:
        df_validation_pred = df_validation_pred.set_index(CHEM_ID).sort_index()

    # get X and y
    X_mbval_structure = df_validation_true[feature_names]
    X_mbval_sirius = df_validation_pred[feature_names]
    y_mbval = df_validation_true[target_variable].astype(np.uint8)

    return (
        X_mbval_structure,
        X_mbval_sirius,
        y_mbval,
    )


def split_training_data(
    X,
    y,
    cluster,
    train_test_split_ratio,
    random_state,
):
    from sklearn.model_selection import train_test_split

    # get single member clusters
    cluster_counts = cluster.value_counts()
    single_member_clusters = cluster_counts[cluster_counts == 1].index
    single_member_indices = [
        cluster[cluster == i].index[0] for i in single_member_clusters
    ]
    X_single = X[X.index.isin(single_member_indices)]
    y_single = y[y.index.isin(single_member_indices)]
    X_multiple = X[~X.index.isin(single_member_indices)]
    y_multiple = y[~y.index.isin(single_member_indices)]
    cluster_multiple = cluster[~cluster.index.isin(single_member_indices)]
    print(X.shape, X_single.shape, y.shape, y_single.shape)
    print(X.shape, X_multiple.shape, y.shape, y_multiple.shape)

    # stratify multiple clusters data
    stratify = cluster_multiple
    X_train, X_test, y_train, y_test = train_test_split(
        X_multiple,
        y_multiple,
        test_size=train_test_split_ratio,
        random_state=random_state,
        shuffle=True,  # shuffle the data before splitting (default)
        stratify=stratify,
    )

    # add single clusters to training data
    X_train = pd.concat([X_train, X_single], ignore_index=True)
    y_train = pd.concat([y_train, y_single], ignore_index=True)
    print(X_train.shape, y_train.shape, X_test.shape, y_test.shape)

    return X_train, y_train, X_test, y_test


def handle_oversampling(
    X,
    y,
    random_state,
):
    from imblearn.over_sampling import RandomOverSampler

    ros = RandomOverSampler(random_state=random_state)
    X, y = ros.fit_resample(X, y)
    return X, y


class RemoveCorrelatedFeatures(BaseEstimator, TransformerMixin):
    def __init__(self, threshold=0.9):
        self.threshold = threshold
        self.correlated_features = set()

    def fit(self, X, y=None):
        corr_matrix = np.corrcoef(X, rowvar=False)
        for i in range(len(corr_matrix)):
            for j in range(i + 1, len(corr_matrix)):
                if abs(corr_matrix[i, j]) > self.threshold:
                    self.correlated_features.add(j)
        return self

    def transform(self, X, y=None):
        return np.delete(X, list(self.correlated_features), axis=1)


def build_preprocessing_pipeline(
    feature_selection,
    remove_lowvariance_features,
    remove_highcorrelation_features,
    variance_threshold,
    correlation_threshold,
    random_state,
):
    from sklearn.feature_selection import VarianceThreshold
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.feature_selection import SelectFromModel

    preprocessing_pipeline_steps = []
    if feature_selection:
        if remove_lowvariance_features:
            # remove all low-variance features
            feature_selection_variance_threshold = VarianceThreshold(variance_threshold)
            preprocessing_pipeline_steps.append(
                (
                    "feature_selection_variance_threshold",
                    feature_selection_variance_threshold,
                )
            )

        if remove_highcorrelation_features:
            # remove correlated features
            remove_correlated_features = RemoveCorrelatedFeatures(
                threshold=correlation_threshold
            )
            preprocessing_pipeline_steps.append(
                (
                    "remove_correlated_features",
                    remove_correlated_features,
                )
            )

        feature_selection_model = RandomForestClassifier(random_state=random_state)

        feature_selection_from_model = SelectFromModel(
            estimator=feature_selection_model, threshold="mean"
        )

        preprocessing_pipeline_steps.append(
            ("feature_selection_from_model", feature_selection_from_model)
        )

    preprocessing_pipeline = Pipeline(preprocessing_pipeline_steps)
    LOGGER.info("Built Preprocessing pipeline (feature selection)")
    return [preprocessing_pipeline]


def preprocess_all_sets(
    preprocessing_pipeline,
    feature_names,
    X_train_os,
    y_train_os,
    X_train,
    X_test,
    X_mbval_structure,
    X_mbval_sirius,
):
    # Feature selection fitted on train set. Transform all sets with the same feature selection
    if preprocessing_pipeline.steps:
        X_train_os = preprocessing_pipeline.fit_transform(
            X_train_os,
            y_train_os,
        )

        num_features = X_train_os.shape[1]
        LOGGER.info(f"Number of selected features: {num_features}")

        # Get the selected feature indices and then names
        selected_feature_indices = preprocessing_pipeline[-1].get_support()
        selected_feature_names = [
            feature_names[i]
            for i, selected in enumerate(selected_feature_indices)
            if selected
        ]
        selected_feature_df = pd.DataFrame(selected_feature_names, columns=["feature"])
        selected_feature_df.to_csv(
            Path(DUMP_FOLDER) / "selected_features.csv", index=False
        )

        # Transform other sets (e.g. subselect feature columns that were selected by the feature selection model)
        X_train = preprocessing_pipeline.transform(X_train)
        X_test = preprocessing_pipeline.transform(X_test)
        X_mbval_structure = preprocessing_pipeline.transform(X_mbval_structure)
        X_mbval_sirius = preprocessing_pipeline.transform(X_mbval_sirius)

        # Assert that all sets have the same features
        if (
            num_features != X_train.shape[1]
            or num_features != X_test.shape[1]
            or num_features != X_mbval_structure.shape[1]
            or num_features != X_mbval_sirius.shape[1]
        ):
            LOGGER.error(
                f"Number of features in train, test, mbval_structure, mbval_sirius do not match: "
                f"{num_features}, {X_train.shape[1]}, {X_test.shape[1]}, {X_mbval_structure.shape[1]}, {X_mbval_sirius.shape[1]}"
            )
            raise RuntimeError("Error in feature selection")

    # Save preprocessing_model
    preprocessing_model_path = Path(DUMP_FOLDER) / "preprocessing_model.joblib"
    joblib.dump(preprocessing_pipeline, preprocessing_model_path, compress=3)

    return (
        selected_feature_names,
        X_train_os,
        X_train,
        X_test,
        X_mbval_structure,
        X_mbval_sirius,
    )


def log_binarized_label_count(y, title, activity_threshold):
    # Ensure y is compared activity_threshold to produce a boolean Series
    y_binarized = y >= activity_threshold

    # Use value_counts() to count both True and False explicitly, ensuring no missing values
    counts = (
        y_binarized.value_counts(dropna=False)
        .reindex([False, True], fill_value=0)
        .values
    )

    # Log the counts. Note: `counts[0]` represents False (inactive), `counts[1]` represents True (active)
    LOGGER.info(
        f"Binarized Label Count {title}: {len(y)} datapoints"
        f" with {counts[0]} inactive, {counts[1]} active "
        f"({counts[1] / sum(counts) * 100:.2f}%)"
    )


def build_pipeline(estimator, random_state):
    pipeline_steps = []
    for i, step in enumerate(estimator["steps"]):
        step_name = step["name"]
        step_args = step.get("args", {})  # get the hyperparameters for the step, if any
        step_args.update({"random_state": random_state})
        step_instance = globals()[step_name](
            **step_args
        )  # dynmically create an instance of the step
        pipeline_steps.append((step_name, step_instance))

    pipeline = Pipeline(pipeline_steps)
    LOGGER.info("=" * 100 + "\n")
    LOGGER.info(f"Built Pipeline for {ESTIMATOR_PIPELINE}")
    return pipeline


def build_param_grid(estimator_steps):
    param_grid = {}
    for step in estimator_steps:
        step_name = step["name"]
        step_args = step.get("args", {})
        param_grid.update(
            {
                f"{step_name}__{key}": value
                for key, value in step_args.items()
                if isinstance(value, list)
            }
        )
    return param_grid


def perform_grid_search_cv(
    X_train, y_train, estimator, pipeline, n_splits, n_repeats, random_state
):
    from sklearn.model_selection import GridSearchCV, RepeatedStratifiedKFold

    cv = RepeatedStratifiedKFold(
        n_splits=n_splits,
        n_repeats=n_repeats,
        random_state=random_state,
    )

    grid_search_cv = GridSearchCV(
        pipeline,
        param_grid=build_param_grid(estimator["steps"]),
        cv=cv,
        scoring=None,
        n_jobs=-1,
        verbose=3,
    )

    # Use train set as input to Grid Search Cross Validation
    # (k-fold cross-validation sets drawn internally from train set)
    grid_search_cv = grid_search_cv.fit(X_train, y_train)

    LOGGER.info(f"{estimator['name']}: GridSearchCV Results:")
    best_params = (
        grid_search_cv.best_params_ if grid_search_cv.best_params_ else "default"
    )
    LOGGER.info(f"Best params: {best_params}")
    LOGGER.info(f"With scorer=None: {grid_search_cv.best_score_}")

    return grid_search_cv


def custom_cost_to_minimize(
    cost_tpr,
    tpr,
    cost_fpr,
    fpr,
):
    return cost_tpr * (1 - tpr) + cost_fpr * fpr


def find_optimal_threshold_roc(
    y,
    y_pred_proba,
    default_threshold,
    threshold_moving,
    target_tpr,
    target_tnr,
    cost_tpr,
    cost_fpr,
):
    from sklearn.metrics import roc_curve

    # get ROC curve
    fpr, tpr, thresholds_roc = roc_curve(y, y_pred_proba)

    # get thresholds from ROC curve
    df_fpr_tpr = pd.DataFrame({"FPR": fpr, "TPR": tpr, "Threshold": thresholds_roc})
    idx_default = np.argmin(np.abs(thresholds_roc - default_threshold))
    if threshold_moving:
        idx_tpr = np.argmax(tpr >= target_tpr)
        fixed_threshold_tpr = thresholds_roc[idx_tpr]
        tnr = 1 - fpr
        idx_tnr = np.abs(tnr - target_tnr).argmin()
        fixed_threshold_tnr = thresholds_roc[idx_tnr]
        costs = custom_cost_to_minimize(cost_tpr, tpr, cost_fpr, fpr)
        optimal_idx = np.argmin(costs)
        optimal_threshold = thresholds_roc[optimal_idx]

    # generate curve
    plt.figure(figsize=(8, 8))
    fontsize = 12
    plt.scatter(
        df_fpr_tpr["FPR"], df_fpr_tpr["TPR"], s=5, alpha=0.8, color="black", zorder=2
    )

    plt.plot(
        df_fpr_tpr["FPR"],
        df_fpr_tpr["TPR"],
        linestyle="-",
        alpha=0.8,
        color="black",
        zorder=2,
        label=f"{ESTIMATOR_PIPELINE}",
    )

    # No-Skill classifier
    plt.plot(
        [0, 1],
        [0, 1],
        linestyle="--",
        color="gray",
        alpha=0.8,
        label="No-skill classifier",
    )

    # Highlight thresholds point
    plt.scatter(
        fpr[idx_default],
        tpr[idx_default],
        alpha=0.8,
        color="blue",
        s=120,
        marker="o",
        label=f"Default threshold: {default_threshold}",
    )
    if threshold_moving:
        plt.scatter(
            fpr[optimal_idx],
            tpr[optimal_idx],
            alpha=0.8,
            color="green",
            s=120,
            marker="o",
            label=f"Optimal threshold: {optimal_threshold:.3f}",
        )
        plt.scatter(
            fpr[idx_tpr],
            tpr[idx_tpr],
            alpha=0.8,
            color="orange",
            s=120,
            marker="o",
            label=f"TPR≈{target_tpr} threshold: {fixed_threshold_tpr:.3f}",
        )
        plt.scatter(
            fpr[idx_tnr],
            tpr[idx_tnr],
            alpha=0.8,
            color="red",
            s=120,
            marker="o",
            label=f"TNR≈{target_tnr} threshold: {fixed_threshold_tnr:.3f}",
        )

    info_text = (
        f"Info:\n"
        f"        TPR = TP / (TP + FN)\n"
        f"        FPR = FP / (FP + TN)\n"
        f"        TNR = 1 - FPR\n"
        f"        Optimal Cost(TPR, FPR) =\n"
        f"        {cost_tpr} * (1 - TPR) + {cost_fpr} * FPR"
    )
    plt.plot([1, 1], [1, 1], linestyle="", alpha=0.0, label=f"{info_text}")

    plt.legend(fontsize=fontsize, loc="lower right", framealpha=0.6)
    plt.xlim(-0.01, 1)
    plt.ylim(0, 1.01)
    plt.xlabel("False Positive Rate (FPR)", fontsize=fontsize + 2)
    plt.ylabel("True Positive Rate (TPR)", fontsize=fontsize + 2)
    plt.xticks(fontsize=fontsize - 1)
    plt.yticks(fontsize=fontsize - 1)
    plt.title(f"aeid: {AEID}", fontsize=fontsize + 3)

    plt.grid()
    plt.tight_layout()

    plt.savefig(Path(DUMP_FOLDER) / "roc_curve.svg", format="svg")
    plt.close("all")

    # create and store dataframe with thresholds
    if threshold_moving:
        thresholds_list = [
            default_threshold,
            optimal_threshold,
            fixed_threshold_tpr,
            fixed_threshold_tnr,
        ]
        thresholds_df = pd.DataFrame(
            {
                "threshold": thresholds_list,
                "threshold_name": ["default", "optimal", "tpr", "tnr"],
            }
        )
        thresholds_df.round(5).to_csv(Path(DUMP_FOLDER) / "thresholds.csv", index=False)
        LOGGER.info("Optimal and fixed threshold saved.")

        return optimal_threshold, fixed_threshold_tpr, fixed_threshold_tnr

    else:
        return None, None, None


def plot_precision_recall_curve(
    y,
    y_pred_proba,
    default_threshold,
):
    from sklearn.metrics import precision_recall_curve

    # get precision recall curve
    prec, recall, thresholds_pr = precision_recall_curve(y, y_pred_proba)
    #    thresholds_pr = np.append(thresholds_pr, thresholds_pr[-1])

    # create dataframe
    df_pr = pd.DataFrame(
        {"Precision": prec[:-1], "Recall": recall[:-1], "Threshold": thresholds_pr}
    )
    idx_default = np.argmin(np.abs(thresholds_pr - default_threshold))

    # generate curve
    plt.figure(figsize=(8, 8))
    fontsize = 12
    plt.scatter(
        df_pr["Recall"], df_pr["Precision"], s=5, alpha=0.8, color="black", zorder=2
    )

    plt.plot(
        df_pr["Recall"],
        df_pr["Precision"],
        linestyle="-",
        alpha=0.8,
        color="black",
        zorder=2,
        label=f"{ESTIMATOR_PIPELINE}",
    )

    # No-Skill classifier
    npos_rel = len(y[y == 1]) / len(y)
    plt.plot(
        [0, 1],
        [npos_rel, npos_rel],
        linestyle="--",
        color="gray",
        alpha=0.8,
        label="No-skill classifier",
    )

    # Highlight thresholds point
    plt.scatter(
        recall[idx_default],
        prec[idx_default],
        alpha=0.8,
        color="blue",
        s=120,
        marker="o",
        label=f'"Default" threshold: {default_threshold}',
    )

    plt.legend(fontsize=fontsize, loc="lower left", framealpha=0.6)
    plt.xlim(-0.01, 1)
    plt.ylim(0, 1.01)
    plt.xlabel("Recall", fontsize=fontsize + 2)
    plt.ylabel("Precision", fontsize=fontsize + 2)
    plt.xticks(fontsize=fontsize - 1)
    plt.yticks(fontsize=fontsize - 1)
    plt.title(f"aeid: {AEID}", fontsize=fontsize + 3)

    plt.grid()
    plt.tight_layout()

    plt.savefig(Path(DUMP_FOLDER) / "pr_curve.svg", format="svg")
    plt.close("all")


def predict_and_report_classification(
    X,
    y,
    best_estimator,
    default_threshold,
    threshold_moving,
    target_tpr,
    target_tnr,
    cost_tpr,
    cost_fpr,
    cmap="Blues",
):
    from sklearn.metrics import (
        precision_score,
        recall_score,
        f1_score,
        balanced_accuracy_score,
        average_precision_score,
        roc_auc_score,
        matthews_corrcoef,
        classification_report,
        confusion_matrix,
        ConfusionMatrixDisplay,
    )

    # Get the prediction probabilites
    y_pred_proba = best_estimator.predict_proba(X)[:, 1]

    # Get the predictions for the default threshold
    LOGGER.info(f"Default threshold: {default_threshold}")
    y_pred_default_threshold = np.where(y_pred_proba >= default_threshold, 1, 0)

    # Get common metrics
    support = len(y)
    n_pos = np.sum(y)
    f1_micro = f1_score(y, y_pred_default_threshold, average="micro")
    f1_macro = f1_score(y, y_pred_default_threshold, average="macro")
    recall_micro = recall_score(y, y_pred_default_threshold, average="micro")
    recall_macro = recall_score(y, y_pred_default_threshold, average="macro")
    precision_micro = precision_score(y, y_pred_default_threshold, average="micro")
    precision_macro = precision_score(y, y_pred_default_threshold, average="macro")
    balanced_accuracy = balanced_accuracy_score(y, y_pred_default_threshold)
    mcc = matthews_corrcoef(y, y_pred_default_threshold)
    pr_auc = average_precision_score(y, y_pred_proba)
    roc_auc = roc_auc_score(y, y_pred_proba)

    # Save the metrics
    metrics_df = pd.DataFrame(
        {
            "support": [support],
            "n_pos": [n_pos],
            "recall_micro": [recall_micro],
            "recall_macro": [recall_macro],
            "precision_micro": [precision_micro],
            "precision_macro": [precision_macro],
            "f1_micro": [f1_micro],
            "f1_macro": [f1_macro],
            "balanced_accuracy": [balanced_accuracy],
            "mcc": [mcc],
            "pr_auc": [pr_auc],
            "roc_auc": [roc_auc],
        }
    )
    metrics_df.round(5).to_csv(Path(DUMP_FOLDER) / "metrics.csv", index=False)

    # concatenate true values and predictions
    data = {
        "Actual": y,
        "Prediction Probability": y_pred_proba,
        "Prediction Default": y_pred_default_threshold,
    }

    # start lists for predictions
    y_preds = [y_pred_default_threshold]
    y_preds_names = ["default"]
    y_preds_descs = [f"Classification Threshold default={default_threshold}"]

    # Precision recall curve
    plot_precision_recall_curve(
        y,
        y_pred_proba,
        default_threshold=default_threshold,
    )

    # Adjust predictions based on classification threshold
    # ROC curve
    (
        optimal_threshold,
        fixed_threshold_tpr,
        fixed_threshold_tnr,
    ) = find_optimal_threshold_roc(
        y,
        y_pred_proba,
        default_threshold,
        threshold_moving,
        target_tpr=target_tpr,
        target_tnr=target_tnr,
        cost_tpr=cost_tpr,
        cost_fpr=cost_fpr,
    )
    LOGGER.info(f"Optimal threshold: {optimal_threshold}")
    LOGGER.info(f"Fixed threshold TPR≈{target_tpr}: {fixed_threshold_tpr}")
    LOGGER.info(f"Fixed threshold, TNR≈{target_tnr}: {fixed_threshold_tnr}")

    if threshold_moving:
        y_pred_optimal_threshold = np.where(y_pred_proba >= optimal_threshold, 1, 0)
        y_pred_fixed_threshold_tpr = np.where(y_pred_proba >= fixed_threshold_tpr, 1, 0)
        y_pred_fixed_threshold_tnr = np.where(y_pred_proba >= fixed_threshold_tnr, 1, 0)

        y_preds += [
            y_pred_optimal_threshold,
            y_pred_fixed_threshold_tpr,
            y_pred_fixed_threshold_tnr,
        ]
        y_preds_names += ["optimal", "tpr", "tnr"]
        y_preds_descs += [
            "Classification Threshold by cost(TPR, TNR)",
            f"Classification Threshold by TPR≈{target_tpr}",
            f"Classification Threshold by TNR≈{target_tnr}",
        ]

        new_data = {
            "Prediction Optimal": y_pred_optimal_threshold,
            "Prediction TPR": y_pred_fixed_threshold_tpr,
            "Prediction TNR": y_pred_fixed_threshold_tnr,
        }
        data.update(new_data)
        # data = pd.DataFrame(data)

    # df = pd.DataFrame(data)
    # df.round(5).to_csv(os.path.join(DUMP_FOLDER, "estimator_results.csv"), index=False)

    # Confusion Matrix
    labels = [True, False]
    for i, y_pred in enumerate(y_preds):
        LOGGER.info("." * 40)
        LOGGER.info(f"Predict {y_preds_names[i]}")
        name = y_preds_names[i]
        desc = y_preds_descs[i]
        report_dict = classification_report(
            y,
            y_pred,
            labels=labels,
            output_dict=True,
        )
        report_df = pd.DataFrame(report_dict).transpose()
        report_df.round(5).to_csv(Path(DUMP_FOLDER) / f"report_{name}.csv")

        cm = confusion_matrix(
            y,
            y_pred,
            labels=labels,
        )
        tn, fp, fn, tp = cm.ravel()  # Extract values from confusion matrix
        LOGGER.info(f"Total: {len(y)} datapoints")
        LOGGER.info(f"Ground truth: {tp + fn} positive, {tn + fp} negative")
        LOGGER.info(f"Prediction: {tp + fp} positive, {tn + fn} negative")

        display_labels = {
            "Positive": {"fontsize": 30},
            "Negative": {"fontsize": 30},
        }

        plt.figure(figsize=(8, 8))
        cm_display = ConfusionMatrixDisplay(
            confusion_matrix=cm, display_labels=display_labels
        )
        cm_display.plot(cmap=cmap, colorbar=False)

        pos_count = cm[0, 0] + cm[0, 1]
        neg_count = cm[1, 0] + cm[1, 1]

        plt.suptitle(f"Confusion Matrix: {desc} ", fontsize=10)
        plt.title(
            f"aeid: {AEID}, {ESTIMATOR_PIPELINE}, Count: {len(y)} (P:{pos_count}, N:{neg_count})",
            fontsize=10,
        )
        plt.savefig(Path(DUMP_FOLDER) / f"cm_{name}.svg", format="svg")
        plt.close("all")


class ElapsedTimeFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style="%"):
        super().__init__(fmt, datefmt, style)
        self.start_time = START_TIME

    def format(self, record):
        delta = datetime.now() - self.start_time
        hours, remainder = divmod(delta.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        hundredths = int((delta.microseconds / 10000) % 100)
        elapsed_time_formatted = (
            f"[{int(hours):02}:{int(minutes):02}:{int(seconds):02}:{hundredths:02}]"
        )
        return f"{elapsed_time_formatted} {super().format(record)}"


def get_timestamp(time_point):
    return time_point.strftime("%Y-%m-%d_%H-%M-%S")


def report_exception(exception, traceback_info, entitiy):
    error_file_path = Path(LOG_PATH) / "log/error.error"
    with open(error_file_path, "a") as f:
        err_msg = f"{entitiy} failed: {exception}"
        LOGGER.error(err_msg)
        LOGGER.error(traceback_info)
        print(err_msg, file=f)
        print(traceback_info, file=f)


def save_model(best_estimator, fit_set):
    best_estimator_path = Path(DUMP_FOLDER) / f"best_estimator_{fit_set}.joblib"
    joblib.dump(best_estimator, best_estimator_path, compress=3)


def get_feature_importance_if_applicable(
    best_estimator,
    feature_names,
):
    best_estimator_model = best_estimator[
        -1
    ]  # best_estimator is the pipeline and the last step is the model itself
    try:
        feature_importances = best_estimator_model.feature_importances_
        importance_df = pd.DataFrame(
            {"feature": feature_names, "importances": feature_importances}
        )
        importance_df = importance_df.sort_values(by="importances", ascending=False)
        importance_df.to_csv(
            Path(DUMP_FOLDER) / "sorted_feature_importances.csv", index=False
        )

    except Exception:
        feature_importances = None
        LOGGER.error(f"Feature Importance not implemented for {ESTIMATOR_PIPELINE}")


def _create_empty_log_file(filename):
    with open(filename, "w", encoding="utf-8"):
        pass


def init_logger(logs_folder):
    global LOGGER, LOG_PATH, LOGGER_FOLDER
    # create folder for run
    RUN_FOLDER = get_timestamp(START_TIME)
    LOG_PATH = os.path.join(logs_folder, RUN_FOLDER)
    LOGGER_FOLDER = os.path.join(LOG_PATH, "log")
    os.makedirs(LOGGER_FOLDER, exist_ok=True)
    log_filename = os.path.join(LOGGER_FOLDER, "modelfitting.log")
    error_filename = os.path.join(LOGGER_FOLDER, "modelfitting.error")
    _create_empty_log_file(log_filename)
    _create_empty_log_file(error_filename)

    # setup logger
    file_handler = logging.FileHandler(log_filename, encoding="utf-8")
    console_handler = logging.StreamHandler(stream=sys.stdout)
    formatter = ElapsedTimeFormatter("%(message)s")
    LOGGER.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    LOGGER.addHandler(file_handler)
    LOGGER.addHandler(console_handler)
    return LOGGER, RUN_FOLDER


def add_status_file(status):
    with open(os.path.join(DUMP_FOLDER, f"{status}.txt"), "w") as file:
        file.write(status)


def get_total_elapsed_time():
    elapsed_seconds = round((datetime.now() - START_TIME).total_seconds(), 2)
    hours, remainder = divmod(elapsed_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    elapsed_formatted = f"{int(hours):02}:{int(minutes):02}:{int(seconds):02}"
    return elapsed_formatted
