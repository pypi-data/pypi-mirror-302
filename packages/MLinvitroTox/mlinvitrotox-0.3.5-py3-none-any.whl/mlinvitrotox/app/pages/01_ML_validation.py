import os

from pathlib import Path

import pandas as pd

import streamlit as st

from mlinvitrotox.constants import (
    # MODELS_RESULTS_DIR_PATH,
    # Files
    SELECTED_AEIDS,  # 30
)

# Add a dropdon to the sidebar: Select run folder
logs_folder = Path("data/results/models")
# logs_folder = Path(MODELS_RESULTS_DIR_PATH)
run_folder = st.sidebar.selectbox(
    "Select Run", [run_folder for run_folder in os.listdir(logs_folder)][::-1]
)
run_folder_path = logs_folder / run_folder

# Load logged assay information overview
assay_info_path = run_folder_path / SELECTED_AEIDS
assay_info_df = pd.read_csv(assay_info_path)
aeid_list = sorted(assay_info_df["aeid"].to_list())

# Add a dropdown to the sidebar: Select target variable
target_variable_list = os.listdir(run_folder_path)
target_variable_list = [
    d
    for d in target_variable_list
    if os.path.isdir(run_folder_path / d) and "hitcall" in d
]
if len(target_variable_list) > 1:
    target_variable = st.sidebar.selectbox(
        "Select Target Variable", target_variable_list
    )
else:
    target_variable = target_variable_list[0]
    st.sidebar.write(f"Target variable: {target_variable}")

# Add a dropdown to the sidebar: Select algorithm
target_variable_path = run_folder_path / target_variable
ml_algorithm_list = os.listdir(target_variable_path)
ml_algorithm_list = [
    d for d in ml_algorithm_list if os.path.isdir(target_variable_path / d)
]
if len(ml_algorithm_list) > 1:
    ml_algorithm = st.sidebar.selectbox(
        "Select ML Algorithm",
        ml_algorithm_list,
    )
else:
    ml_algorithm = ml_algorithm_list[0]
    st.sidebar.write(f"Algorithm: {ml_algorithm}")

# Add a dropdown to the sidebar: Select aeid
aeid = str(
    st.sidebar.selectbox(
        "Select AEID",
        aeid_list,
    )
)

# Add a dropdown to the sidebar: Select preprocessing model
aeid_path = target_variable_path / ml_algorithm / aeid
preprocessor_list = os.listdir(aeid_path)
preprocessor_list = [d for d in preprocessor_list if os.path.isdir(aeid_path / d)]
results_available = True
if len(preprocessor_list) == 0:
    st.write("No results for this aeid")
    results_available = False
elif len(preprocessor_list) > 1:
    preprocessor = st.sidebar.selectbox(
        "Select feature selection model", preprocessor_list
    )
else:
    preprocessor = preprocessor_list[0]
    st.sidebar.write(f"Feature selection: {preprocessor.split('_')[2]}")

if results_available:
    # Add a dropdown to the sidebar: Select estimator model
    preprocessor_path = aeid_path / preprocessor
    estimator_list = os.listdir(preprocessor_path)
    estimator_list = [d for d in estimator_list if os.path.isdir(preprocessor_path / d)]
    if len(estimator_list) > 1:
        estimator = st.sidebar.selectbox("Select Estimator Model", estimator_list)
    else:
        estimator = estimator_list[0]
        st.sidebar.write(f"Model: {estimator}")

    # Add a dropdown to the sidebar: Select validation type
    # TODO unify names with validation summary
    estimator_path = preprocessor_path / estimator
    val_type_list = os.listdir(estimator_path)
    val_type_list = [d for d in val_type_list if os.path.isdir(estimator_path / d)]
    val_type = st.sidebar.selectbox(
        "Select Validation Type",
        val_type_list[::-1],
    )

    st.title("Validation Results (using 4 different classification thresholds)")
    info_data = {
        "Target Variable": [target_variable],
        "ML Algorithm": [ml_algorithm],
        "aeid": [aeid],
        "Feature Selection": [preprocessor.split("_")[2]],
        "Estimator": [estimator],
        "Validation Set": [val_type],
    }
    info_df = pd.DataFrame(info_data)
    st.dataframe(info_df, hide_index=True, use_container_width=True)

    # Plot confusion matrices for all 4 classification thresholds
    st.write(val_type)
    val_type_path = estimator_path / val_type
    confusion_matrices_paths = {}
    roc_curve_paths = {}
    reports = {}
    threshold_names = []
    threshold_values = []
    # TODO do not hardcode the classification threshold entries
    for classification_threshold in ["default", "optimal", "tnr", "tpr"]:
        cm_path = val_type_path / f"cm_{classification_threshold}.svg"
        confusion_matrices_paths[classification_threshold] = cm_path

        report_path = val_type_path / f"report_{classification_threshold}.csv"
        reports[classification_threshold] = (
            pd.read_csv(report_path)
            .reset_index(drop=True)
            .rename(columns={"Unnamed: 0": "class"})
        )
        threshold_names.append(classification_threshold)

    roc_path = val_type_path / "roc_curve.svg"
    pr_path = val_type_path / "pr_curve.svg"

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.header("ROC curve")
            st.image(open(roc_path).read())
        with col2:
            st.header("Precision recall curve")
            st.image(open(pr_path).read())

    st.divider()

    # Create a 2x2 grid using columns
    st.header("Confusion matrices for different thresholds")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            i = 0
            st.subheader("Default = 0.5")
            threshold = threshold_names[i]
            cm_path = confusion_matrices_paths[threshold]
            st.image(open(cm_path).read())
            with st.expander("Show classification report"):
                st.dataframe(reports[threshold])
        with col2:
            i = 1
            st.subheader("TNR ≈ 0.5")
            threshold = threshold_names[i]
            cm_path = confusion_matrices_paths[threshold]
            st.image(open(cm_path).read())
            with st.expander("Show classification report"):
                st.dataframe(reports[threshold])

    st.divider()

    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            i = 3
            st.subheader("Cost(TPR, TNR) = 2*(1-TPR) + (1-TNR)")
            threshold = threshold_names[i]
            cm_path = confusion_matrices_paths[threshold]
            st.image(open(cm_path).read())
            with st.expander("Show classification report"):
                st.dataframe(reports[threshold])
        with col2:
            i = 2
            st.subheader("TPR ≈ 0.5")
            threshold = threshold_names[i]
            cm_path = confusion_matrices_paths[threshold]
            st.image(open(cm_path).read())
            with st.expander("Show classification report"):
                st.dataframe(reports[threshold])

    st.divider()
