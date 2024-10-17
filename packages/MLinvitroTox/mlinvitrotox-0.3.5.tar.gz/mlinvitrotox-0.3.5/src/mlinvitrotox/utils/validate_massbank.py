# Data processing: 4) massbank validation of sirius

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib
from matplotlib import pyplot as plt

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    matthews_corrcoef,
)

from mlinvitrotox.constants import (
    # IDs
    MASSBANK_ID,
)

# Setup
matplotlib.use("Agg")


def load_massbank_val_df(input_path):
    # Load dataframe
    df = pd.read_parquet(input_path)
    # df = pd.read_csv(input_path)

    return df


# Identify shared GUIDs
def filter_mbval_dfs(df_true, df_pred):
    """
    Filter MassBank validation dataframs to only contain shared chemicals (by GUID)

    """

    # get shared GUIDs between the two data frames
    true_fps_guids = set(df_true[MASSBANK_ID])
    pred_fps_guids = set(df_pred[MASSBANK_ID])
    shared_guids = true_fps_guids.intersection(pred_fps_guids)
    shared_guids_list = list(shared_guids)

    # Filter and sort dataframes (only keep entries with shared GUIDs)
    df_true_filtered = df_true[
        df_true[MASSBANK_ID].isin(shared_guids_list)
    ].sort_values(by=MASSBANK_ID)
    df_pred_filtered = df_pred[
        df_pred[MASSBANK_ID].isin(shared_guids_list)
    ].sort_values(by=MASSBANK_ID)

    # Set GUID as index
    df_true_filtered.set_index(MASSBANK_ID, inplace=True)
    df_pred_filtered.set_index(MASSBANK_ID, inplace=True)

    return df_true_filtered, df_pred_filtered


# Define tanimoto coefficient function
def tanimoto_coefficient(fp1, fp2):
    """
    helper function to calculate Tanimoto coefficient of two fingerprints

    """
    fp1 = np.array(fp1)
    fp2 = np.array(fp2)
    intersection = np.sum(np.logical_and(fp1, fp2))
    union = np.sum(np.logical_or(fp1, fp2))
    if union == 0:
        return 0.0

    return intersection / float(union)


# Calculate metrics for each GUID
def calculate_metrics_per_chemical(df_true, df_pred, output_metrics):
    # initialize
    df = pd.DataFrame(
        index=df_true.index,
        columns=["Tanimoto", "Accuracy", "Precision", "Recall", "F1", "MCC"],
    )

    # Define columns to consider (excluding GUID as it is now an index)
    fp_columns = [col for col in df_true.columns if col.isdigit()]

    # calculate metrics for each chemical
    for guid in df_true.index:
        fps_true = df_true.loc[guid, fp_columns].astype(int)
        fps_pred = df_pred.loc[guid, fp_columns].astype(int)

        y_true = fps_true.to_numpy().flatten()
        y_pred = fps_pred.to_numpy().flatten()

        df.loc[guid, "Tanimoto"] = tanimoto_coefficient(y_true, y_pred)
        df.loc[guid, "Accuracy"] = (
            accuracy_score(y_true, y_pred)
            if np.any(y_true) or np.any(y_pred)
            else np.nan
        )
        df.loc[guid, "Precision"] = precision_score(y_true, y_pred, zero_division=0)
        df.loc[guid, "Recall"] = recall_score(y_true, y_pred, zero_division=0)
        df.loc[guid, "F1"] = f1_score(y_true, y_pred, zero_division=0)
        df.loc[guid, "MCC"] = (
            matthews_corrcoef(y_true, y_pred)
            if np.any(y_true) or np.any(y_pred)
            else np.nan
        )
        df.select_dtypes(include=[np.number]).astype(float)

    # Save metrics to file
    df.rename_axis(MASSBANK_ID).sort_index().reset_index().round(5).to_csv(
        output_metrics, index=False
    )

    return df


def generate_discrepancy_figure(df_true, df_pred, output_figure):
    # Initialize an empty DataFrame for discrepancies
    discrepancy_matrix = pd.DataFrame(0, index=df_true.index, columns=df_true.columns)

    # Iterate through each GUID and column to find discrepancies
    for guid in df_true.index:
        for column in df_true.columns:
            true_bit = df_true.at[guid, column]
            pred_bit = df_pred.at[guid, column]

            if true_bit != pred_bit:
                discrepancy_matrix.at[guid, column] = -1 if true_bit == 1 else 1

    # Plot the discrepancy matrix using a heatmap
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.set_title(
        "Discrepancies between true and predicted fingerprint bits", fontsize=16
    )
    ax.set_xlabel("Fingerprint index")
    ax.set_ylabel("GUID")
    ax.set_yticklabels([])

    sns.heatmap(discrepancy_matrix, cmap=["blue", "white", "green"], cbar=False, ax=ax)

    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig(output_figure, format="png")
    plt.close("all")


def calculate_metrics_per_bit(df_true, df_pred, output_metrics):
    # initialize
    df = pd.DataFrame(
        columns=["Accuracy", "Precision", "Recall", "F1", "MCC"],
        index=df_true.columns,
    )

    # calculate metrics for each column
    for column in df_true.columns:
        y_true = df_true[column].to_numpy()
        y_pred = df_pred[column].to_numpy()

        # Calculate metrics for each column
        accuracy = (
            accuracy_score(y_true, y_pred)
            if np.any(y_true) or np.any(y_pred)
            else np.nan
        )
        precision = precision_score(y_true, y_pred, zero_division=0)
        recall = recall_score(y_true, y_pred, zero_division=0)
        f1 = f1_score(y_true, y_pred, zero_division=0)
        mcc = (
            matthews_corrcoef(y_true, y_pred)
            if np.any(y_true) or np.any(y_pred)
            else np.nan
        )

        # Assign metrics to the DataFrame
        df.at[column, "Accuracy"] = accuracy
        df.at[column, "Precision"] = precision
        df.at[column, "Recall"] = recall
        df.at[column, "F1"] = f1
        df.at[column, "MCC"] = mcc

    # store output
    df.rename_axis("absoluteIndex").sort_index().reset_index().round(5).to_csv(
        output_metrics, index=False
    )

    return df


def plot_metrics_histogram(df_column_metrics, output_figure):
    plt.figure(figsize=(10, 6))
    colors = ["red", "green", "blue", "purple", "orange"]
    alpha = 0.5
    bins = 20

    for i, metric in enumerate(df_column_metrics.columns):
        plt.hist(
            df_column_metrics[metric].dropna(),
            bins=bins,
            alpha=alpha,
            label=metric,
            color=colors[i],
        )
    plt.title("Histogram of metrics across fingerprint bits")
    plt.xlabel("Metric value")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_figure, format="png")
    plt.close()


def plot_metrics_density(df_column_metrics, output_figure):
    plt.figure(figsize=(10, 6))
    colors = ["red", "green", "blue", "purple", "orange"]

    for i, metric in enumerate(df_column_metrics.columns):
        sns.kdeplot(
            df_column_metrics[metric].dropna(), color=colors[i], label=metric, fill=True
        )
    plt.title("Density distribution of metrics across fingerprint bits")
    plt.xlabel("Metric value")
    plt.ylabel("Density")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_figure, format="png")
    plt.close()


def save_indexes_passed_validation(
    df_metrics_bit, threshold_recall, threshold_precision, output_file
):
    passed_validation = df_metrics_bit[
        (df_metrics_bit["Recall"] > threshold_recall)
        & (df_metrics_bit["Precision"] > threshold_precision)
    ]
    df_indexes_passed = pd.DataFrame(passed_validation.index, columns=["absoluteIndex"])
    print(f"Initial number of AbsoluteIndexes: {df_metrics_bit.shape}")
    print(f"Filtered number of AbsoluteIndexes: {df_indexes_passed.shape}")

    # store output
    df_indexes_passed.to_csv(output_file, index=False)
