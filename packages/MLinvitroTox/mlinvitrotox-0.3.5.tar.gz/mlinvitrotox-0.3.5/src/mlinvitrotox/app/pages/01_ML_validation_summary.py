import os

from pathlib import Path

import numpy as np
import pandas as pd

import plotly.express as px

import streamlit as st

import mlinvitrotox.app.helper as app

from mlinvitrotox.constants import (
    # Paths
    # MODELS_RESULTS_DIR_PATH,
    # RESULTS_DIR_PATH,
    # Files
    SELECTED_AEIDS,
)

# reverse renaming dictionary
dict_reverse_rename = {v: k for k, v in app.dict_rename.items()}

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
aeid_list = [str(i) for i in sorted(assay_info_df["aeid"].to_list())]
assay_info_df["aeid"] = assay_info_df["aeid"].astype("str")

# Load metrics
metrics_path = run_folder_path / "modeltraining_metrics.csv"
# metrics_path = Path(RESULTS_DIR_PATH) / "predictions" / f"{run_folder}_metrics.csv"
metrics_df = pd.read_csv(metrics_path)
metrics_df["aeid"] = metrics_df["aeid"].astype("str")

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

# Select dummy AEID
# TODO how to select it well?
dummy_aeid = str(100)

# Add a dropdown to the sidebar: Select preprocessing model
aeid_path = target_variable_path / ml_algorithm / dummy_aeid
preprocessor_list = os.listdir(aeid_path)
preprocessor_list = [d for d in preprocessor_list if os.path.isdir(aeid_path / d)]
if len(preprocessor_list) > 1:
    preprocessor = st.sidebar.selectbox(
        "Select feature selection model", preprocessor_list
    )
else:
    preprocessor = preprocessor_list[0]
    st.sidebar.write(f"Feature selection: {preprocessor.split('_')[2]}")

# Add a dropdown to the sidebar: Select validation type
# TODO unify names with other dashboard page
val_type = st.sidebar.selectbox(
    "Select validation set",
    [
        "Internal validation",
        "MB validation from structure",
        "MB validation SIRIUS-predicted",
    ],
)
reverse_val_type = dict_reverse_rename[val_type]

st.sidebar.divider()

# Add selectboxes for x and y axes metrics
# TODO or have another system to choose x and y
metrics = [
    "Recall (macro)",
    "Precision (macro)",
    "F1 (macro)",
    "Recall (micro)",
    "Precision (micro)",
    "F1 (micro)",
    "Balanced Accuracy",
    "ROC AUC",
    "PR AUC",
]
x_metric = st.sidebar.selectbox(
    "Select metric for x-axis",
    metrics,
)
y_metric = st.sidebar.selectbox(
    "Select metric for y-axis",
    [m for m in metrics if m != x_metric],
)
st.sidebar.divider()

# Sidebar: Plotting details
marginal_type = st.sidebar.selectbox(
    "Select marginal type",
    ["box", "violin", "rug", "histogram", None],
)
marker_size_category = st.sidebar.selectbox(
    "Select marker size based on",
    [
        "Higher Imbalance = LARGER",
        "Total Support",
        "Support Positive",
        "Support Negative",
        None,
    ],
)

color_palette_mapping = {
    "Plotly": px.colors.qualitative.Plotly,
    "Safe": px.colors.qualitative.Safe,
    "Light24": px.colors.qualitative.Light24,
    "Bold": px.colors.qualitative.Bold,
    "D3": px.colors.qualitative.D3,
    "G10": px.colors.qualitative.G10,
}

marker_symbol = "circle-dot"
opacity = 1.0
marker_line_width = 0.8
marker_line_color = "#000000"
# TODO which color palette? --> Plotly
# TODO find a color palette for all mechanistic targets!
palette = st.sidebar.selectbox(
    "Select color palette",
    list(color_palette_mapping.keys()),
)
palette = color_palette_mapping.get(palette)
autoscale = st.sidebar.checkbox("Autoscale", value=True)


st.title("Summary of validation results")

# set some values
metrics_df["Target Variable"] = app.dict_rename[target_variable]
metrics_df["Feature Selection"] = app.dict_rename[preprocessor.split("_")[2]]
metrics_df["Validation Set"] = app.dict_rename[val_type]

# extract information
# TODO how to get estimator info to metrics_df?
# metrics_df["Estimator"] = metrics_df["Estimator"].apply(lambda x: app.dict_rename[x])
metrics_df["Estimator"] = "XGBoost"

metrics_df = metrics_df.rename(
    columns={
        "recall_micro": "Recall (micro)",
        "recall_macro": "Recall (macro)",
        "precision_micro": "Precision (micro)",
        "precision_macro": "Precision (macro)",
        "f1_micro": "F1 (micro)",
        "f1_macro": "F1 (macro)",
        "balanced_accuracy": "Balanced Accuracy",
        "mcc": "MCC",
        "roc_auc": "ROC AUC",
        "pr_auc": "PR AUC",
        "support": "Total Support",
        "n_pos": "Support Positive",
    }
)
metrics_df["Support Negative"] = (
    metrics_df["Total Support"] - metrics_df["Support Positive"]
)

metrics_df["Imbalance"] = (
    metrics_df["Support Negative"] - metrics_df["Support Positive"]
)
# TODO how is imbalance score calculated?
metrics_df["Imbalance Score"] = (
    metrics_df["Support Positive"] - metrics_df["Support Negative"]
) / metrics_df["Total Support"]
metrics_df["Imbalance Score"] = metrics_df["Imbalance Score"].round(3)

# merge with mechanistic target information
metrics_df = pd.merge(
    metrics_df,
    assay_info_df[["aeid", "assay_component_endpoint_name", "MechanisticTarget"]],
    on="aeid",
    how="left",
)

# Apply the acronym mapping to the DataFrame
metrics_df["MechanisticTargetAcronym"] = metrics_df["MechanisticTarget"].map(
    app.acronym_mapping
)

df = metrics_df.copy()

st.header("Summary figure")

# apply factor for each marker size category
if marker_size_category == "Total Support":
    df["Marker Size"] = df["Total Support"] ** 0.42
elif marker_size_category == "Support Positive":
    df["Marker Size"] = df["Support Positive"] ** 0.55
elif marker_size_category == "Support Negative":
    df["Marker Size"] = df["Support Negative"] ** 0.45
elif marker_size_category == "Higher Imbalance = LARGER":
    df["Marker Size"] = np.abs(df["Imbalance Score"]) * 15
else:
    df["Marker Size"] = 10
df["Marker Size"] = df["Marker Size"].round(3)
# TODO add legend for marker size

histogram_args = (
    {"marginal_x": marginal_type, "marginal_y": marginal_type}
    if marginal_type is not None
    else {}
)

# TODO which hover data?
args = {
    "opacity": opacity,
    "hover_data": [
        "aeid",
        "Validation Set",
        "Precision (micro)",
        "Precision (macro)",
        "Recall (micro)",
        "Recall (macro)",
        "F1 (micro)",
        "F1 (macro)",
        # "Accuracy",
        "Balanced Accuracy",
        "ROC AUC",
        "PR AUC",
        "Total Support",
        "Support Positive",
        "Support Negative",
        "Imbalance Score",
    ],
    "color_discrete_sequence": palette,
    "custom_data": ["Marker Size"],  # Add customdata to match marker size
}

# Define axis font size and margin
axis_font_size = 20.5
margin = 20

# Construct the title string using the selected metrics
title = ""

# Scatter plot
fig = px.scatter(
    df,
    x=x_metric,
    y=y_metric,
    color="MechanisticTargetAcronym",
    **args,
    **histogram_args,
)


# Update the marker size based on the customdata
for j, trace in enumerate(fig.data):
    if "scatter" in trace.type:
        # Get the marker size from the customdata
        marker_size = list(fig.data[j].customdata[:, 0])
        marker_line_color_ = "black" if marker_line_color else None
        marker_line_width_ = marker_line_width if marker_line_color else None
        fig.data[j].update(
            marker=dict(
                symbol=marker_symbol,
                size=marker_size,
                line=dict(color=marker_line_color_, width=marker_line_width_),
            )
        )

# Update axis labels based on selected metrics
fig.update_layout(
    title=title,
    title_font=dict(size=21, color="black"),
    xaxis_title=x_metric,
    yaxis_title=y_metric,
    xaxis_title_font=dict(size=axis_font_size, color="black"),
    yaxis_title_font=dict(size=axis_font_size, color="black"),
    margin=dict(t=margin),
    width=1200,  # Increase the figure width
    height=800,  # Increase the figure height
    legend=dict(
        orientation="h",  # Horizontal orientation
        yanchor="top",  # Anchor legend at the top of its bounding box
        y=-0.2,  # Position legend below the x-axis
        xanchor="center",  # Anchor legend in the center of its bounding box
        x=0.5,  # Center the legend horizontally
        title_text="",  # Remove legend title
    ),
)

if autoscale:
    fig.update_layout(autosize=True)
else:
    fig.update_layout(xaxis=dict(range=[0.0, 1.0]))
    fig.update_layout(yaxis=dict(range=[0.0, 1.0]))

st.plotly_chart(fig, use_container_width=True)


st.subheader("Performance metrics across the target assay endpoints")
metrics_df = metrics_df[
    [
        "aeid",
        "assay_component_endpoint_name",
        "MechanisticTarget",
        "MechanisticTargetAcronym",
        # "Target Variable",
        # "Feature Selection",
        "Total Support",
        "Support Positive",
        "Support Negative",
        "Precision (micro)",
        "Precision (macro)",
        "Recall (micro)",
        "Recall (macro)",
        "F1 (micro)",
        "F1 (macro)",
        "Balanced Accuracy",
        "MCC",
        "ROC AUC",
        "PR AUC",
        "Estimator",
    ]
]
metrics_df = metrics_df.rename(
    columns={
        "aeid": "aeid",
        "assay_component_endpoint_name": "aeid name",
        "MechanisticTarget": "Mech. target",
        "MechanisticTargetAcronym": "MT acronym",
        # "Target Variable": "y",
        # "Feature Selection": "f. s.",
        "Total Support": "Support",
        "Support Positive": "Pos. support",
        "Support Negative": "Neg. support",
        "Precision (micro)": "micro prec.",
        "Precision (macro)": "macro prec.",
        "Recall (micro)": "micro rec.",
        "Recall (macro)": "macro rec.",
        "F1 (micro)": "micro F1",
        "F1 (macro)": "macro F1",
        "Balanced Accuracy": "bacc",
        "MCC": "mcc",
        "ROC AUC": "roc-auc",
        "PR AUC": "pr-auc",
        "Estimator": "model",
    }
)

st.dataframe(metrics_df, use_container_width=True, hide_index=True)

# TODO combine entries per acronym as a list
mechtar_df = (
    df[["MechanisticTargetAcronym", "MechanisticTarget"]]
    .drop_duplicates()
    .sort_values("MechanisticTargetAcronym")
    .reset_index(drop=True)
)
st.markdown("### Mechanistic targets and their acronyms")
st.dataframe(mechtar_df, hide_index=True)


# TODO Why median? When we include aeid in the groupby, it does not actually do a groupby and
#      the median corresponds to the value of the aeid
# st.subheader("Median performance metrics across the target assay endpoints")

# numeric_columns = [
# "Precision (micro)",
# "Precision (macro)",
# "Recall (micro)",
# "Recall (macro)",
# "F1 (micro)",
# "F1 (macro)",
# "Balanced Accuracy",
# "MCC",
# "ROC AUC",
# "PR AUC",
# "Total Support",
# "Support Positive",
# "Support Negative",
# ]

# groupby_columns = [
# "Target Variable",
# "aeid",
# "assay_component_endpoint_name",
# "Feature Selection",
# "Estimator",
# "Validation Set",
# ]
# mechtar_columns = [
# "MechanisticTarget",
# "MechanisticTargetAcronym",
# ]
# grouped_numeric = (
# df[groupby_columns + numeric_columns]
# .groupby(groupby_columns)
# .median()
# .reset_index()
# )
# grouped = pd.merge(
# grouped_numeric,
# df[groupby_columns + mechtar_columns].drop_duplicates(),
# on=groupby_columns,
# )

# grouped["Precision (micro)"] = grouped["Precision (micro)"].apply(lambda x: f"{x:.3f}")
# grouped["Precision (macro)"] = grouped["Precision (macro)"].apply(lambda x: f"{x:.3f}")
# grouped["Recall (micro)"] = grouped["Recall (micro)"].apply(lambda x: f"{x:.3f}")
# grouped["Recall (macro)"] = grouped["Recall (macro)"].apply(lambda x: f"{x:.3f}")
# grouped["F1 (micro)"] = grouped["F1 (micro)"].apply(lambda x: f"{x:.3f}")
# grouped["F1 (macro)"] = grouped["F1 (macro)"].apply(lambda x: f"{x:.3f}")
# grouped["Balanced Accuracy"] = grouped["Balanced Accuracy"].apply(lambda x: f"{x:.3f}")
# grouped["MCC"] = grouped["MCC"].apply(lambda x: f"{x:.3f}")
# grouped["ROC AUC"] = grouped["ROC AUC"].apply(lambda x: f"{x:.3f}")
# grouped["PR AUC"] = grouped["PR AUC"].apply(lambda x: f"{x:.3f}")

# summary = grouped[
# [
# "aeid",
# "assay_component_endpoint_name",
# "MechanisticTarget",
# "MechanisticTargetAcronym",
##"Target Variable",
##"Feature Selection",
# "Total Support",
# "Support Positive",
# "Support Negative",
# "Precision (micro)",
# "Precision (macro)",
# "Recall (micro)",
# "Recall (macro)",
# "F1 (micro)",
# "F1 (macro)",
# "Balanced Accuracy",
# "MCC",
# "ROC AUC",
# "PR AUC",
# "Estimator",
# ]
# ]
# summary = summary.rename(
# columns={
# "aeid": "aeid",
# "assay_component_endpoint_name": "aeid name",
# "MechanisticTarget": "Mech. target",
# "MechanisticTargetAcronym": "MT acronym",
##"Target Variable": "y",
##"Feature Selection": "f. s.",
# "Total Support": "Support",
# "Support Positive": "Pos. support",
# "Support Negative": "Neg. support",
# "Precision (micro)": "micro prec.",
# "Precision (macro)": "macro prec.",
# "Recall (micro)": "micro rec.",
# "Recall (macro)": "macro rec.",
# "F1 (micro)": "micro F1",
# "F1 (macro)": "macro F1",
# "Balanced Accuracy": "bacc",
# "MCC": "mcc",
# "ROC AUC": "roc-auc",
# "PR AUC": "pr-auc",
# "Estimator": "model",
# }
# )


# summary["aeid"] = summary["aeid"].astype("int")
# summary = summary.sort_values("aeid")
# st.dataframe(summary, use_container_width=True, hide_index=True)
