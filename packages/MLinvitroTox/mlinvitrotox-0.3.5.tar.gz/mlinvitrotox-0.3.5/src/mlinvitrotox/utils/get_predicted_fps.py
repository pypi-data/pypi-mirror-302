# Data processing: 3) extract data from sirius

import os

from pathlib import Path

import pandas as pd

from tqdm import tqdm

from mlinvitrotox.constants import (
    # IDs
    MASSBANK_ID,
    SIRIUS_ID,
)


def check_sirius_version(
    df_csi_fpt,
):
    """
    This is a simple check to ensure that the SIRIUS output
    used to train the mlinvitrotox models
    is comparable to the SIRIUS output of the user.

    """

    # can be either provided directly as a file or as a path
    if isinstance(df_csi_fpt, (str, Path)):
        df_csi_fpt = pd.read_csv(df_csi_fpt, sep="\t")

    if not len(df_csi_fpt) == 3878:
        print(
            "Error: The HRMS data have been processed with a different SIRIUS version than used in MLinvitroTox."
        )
        return False
    else:
        return True


def _format_column_name(file_path):
    parts = file_path.split(os.sep)
    main_part_parts = parts[-2].split("_", 1)
    main_part = main_part_parts[0] + "_" + main_part_parts[1].replace("_", "-")
    last_part = parts[-1].split(".")[0]
    return f"{main_part}_{last_part}"


def compute_fps_data(file_path, absoluteIndex, threshold):
    # load fingerprint
    col_name = _format_column_name(str(file_path))
    df = pd.read_csv(file_path, header=None, names=[col_name])

    # check if it's a fingerprint from the positive mode
    if len(df) != 3878:
        print("The fingerprint does not contain exactly 3878 bits", col_name)
        print("It is not from the positive mode and will not be processed.")
        return {}

    # set the absoluteIndexes from df_csi
    df.index = absoluteIndex

    # apply threshold to generate binary features
    df[col_name] = df[col_name].apply(lambda x: 0 if x < threshold else 1)

    # Check corresponding .info file for 'TopCSIScore'
    dict_info = {}
    info_file_path = str(file_path).replace(".fpt", ".info")
    if os.path.exists(info_file_path):
        with open(info_file_path, "r") as info_file:
            lines = info_file.readlines()
            if lines and any(["TopCSIScore" in line for line in lines]):
                dict_info["TopCSIScore"] = "available"
            else:
                dict_info["TopCSIScore"] = "none"

    # get formula rank
    formula_file_path = (
        "/".join(str(file_path).split("/")[:-1]) + "/formula_candidates.tsv"
    )
    if os.path.exists(formula_file_path):
        formula_df = pd.read_csv(formula_file_path, sep="\t")
        if "rank" in formula_df.columns:
            col_rank = "rank"
        elif "formulaRank" in formula_df.columns:
            col_rank = "formulaRank"
        else:
            print("No formula rank information in formula_file_path")
            col_rank = None
        if col_rank is not None:
            precursor = col_name.split("_")[2]
            adduct = col_name.split("_")[3]
            formularank = formula_df[
                (formula_df["precursorFormula"] == precursor)
                & (formula_df["adduct"].str.replace(" ", "") == adduct)
            ][col_rank].iloc[0]
            dict_info["formulaRank"] = formularank

    # concatenate fingerprint with info
    df_info = pd.Series(dict_info).to_frame(name=col_name)
    df_concat = pd.concat((df, df_info), axis=0)
    return {col_name: df_concat}


def read_fps_files(
    input_fpt_directory,
    df_csi,
    threshold=0.5,
    max_workers=None,
):
    # can be either provided directly as a file or as a path
    if isinstance(df_csi, (str, Path)):
        df_csi = pd.read_csv(df_csi, sep="\t")

    # initialize
    fps_data = {}

    # get file paths for .fpt files
    all_fps_files = [
        Path(root) / f
        for root, dirs, files in os.walk(input_fpt_directory)
        for f in files
        if f.endswith(".fpt")
    ]
    # only files in the main feature folders
    all_fps_files = [
        p
        for p in all_fps_files
        if len(p.parents) == (len(input_fpt_directory.parents) + 2)
    ]
    print(f"Found {len(all_fps_files)} .fpt files.")

    absoluteIndex = df_csi["absoluteIndex"].values

    # process files
    if max_workers is None or max_workers > 1:
        import concurrent.futures

        with concurrent.futures.ProcessPoolExecutor(
            max_workers=max_workers
        ) as executor:
            future_to_file_path = [
                executor.submit(compute_fps_data, file_path, absoluteIndex, threshold)
                for file_path in all_fps_files
            ]
            # future_to_file_path = {executor.submit(compute_fps_data, file_path, absoluteIndex, threshold): file_path for file_path in all_fps_files}
            for future in tqdm(
                concurrent.futures.as_completed(future_to_file_path),
                total=len(all_fps_files),
            ):
                # file_path = future_to_file_path[future]
                fps_column = future.result()
                if fps_column:
                    # merge two dictonaries
                    fps_data |= fps_column
    else:
        for file_path in tqdm(all_fps_files, desc="Processing files"):
            fps_column = compute_fps_data(file_path, absoluteIndex, threshold)
            if fps_column:
                # merge two dictonaries
                fps_data |= fps_column

    # store
    if fps_data:
        fps_df = pd.concat(fps_data.values(), axis=1)
        fps_df.columns = list(fps_data.keys())
        print(f"Dataframe with imported fingerprints: {fps_df.shape[1]} entries")

        # transpose and only keep formulaRank 1 entries
        fps_df_transposed = fps_df.T
        fps_df_transposed.columns = [
            str(col).zfill(4) for col in fps_df_transposed.columns
        ]
        fps_df_transposed.reset_index(inplace=True)
        fps_df_transposed.rename(columns={"index": "features"}, inplace=True)
        if "formulaRank" in fps_df_transposed.columns:
            fps_df_transposed = fps_df_transposed[
                fps_df_transposed["formulaRank"] == 1
            ].copy()

        # extract information from features column
        fps_df_transposed = _extract_info_from_features_column(
            fps_df_transposed,
        )

        # sort to have reproducible output
        fps_df_sorted = fps_df_transposed.sort_values(["features"])

        return fps_df_sorted

    else:
        print("No valid data extracted from .fpt files.")
        return pd.DataFrame()


def keep_selected_fps_bits(
    df_predfps,
    df_truefps,
):
    # only keep fingerprint bits used in training data
    df_truefps.columns = df_truefps.columns.astype(str)
    df_predfps.columns = df_predfps.columns.astype(str)
    columns_to_keep = [
        col
        for col in df_predfps.columns
        if col
        in [
            "features",
            "TopCSIScore",
            "formulaRank",
            SIRIUS_ID,
            MASSBANK_ID,
            "sirius_run",
            "formula",
            "adduct",
        ]
    ]
    columns_to_keep += df_predfps.columns[
        df_predfps.columns.isin(df_truefps.columns)
    ].tolist()
    df_predfps_selected = df_predfps.loc[:, columns_to_keep]

    print(
        f"Dataframe with provided fingerprints: {df_predfps_selected.shape[0]} entries, {df_predfps_selected.shape[1]} fingerprint bits"
    )

    return df_predfps_selected


def _extract_info_from_features_column(df):
    # Split features
    split_df = df["features"].str.split("_", expand=True)

    # Assign columns based on the number of parts found in the split
    df[SIRIUS_ID] = split_df[0]
    df["sirius_run"] = split_df[1]
    df["formula"] = split_df[2]

    # For rows with more than three splits, assign the fourth part to 'adduct', else None
    if len(split_df.columns) <= 3:
        print(split_df)
    df["adduct"] = split_df[3] if len(split_df.columns) > 3 else None

    return df


def filter_mbval_data_by_accession(
    df,
    input_massbank_validation,
):
    # add adjusted sirius run column
    df["adjusted_sirius_run"] = (
        df["sirius_run"].str.split("-", n=3).str[:3].str.join("-")
    )

    # load MassBank validation file
    df_massbank_validation = pd.read_csv(input_massbank_validation)
    df_cut = df_massbank_validation[["ACCESSION", MASSBANK_ID]]

    # merge with input df
    merged_df = pd.merge(
        df,
        df_cut,
        left_on="adjusted_sirius_run",
        right_on="ACCESSION",
        how="inner",
    )
    return merged_df


# aggregate fingerprints for MassBank validation data
def custom_agg(x):
    if x.name.isdigit():
        return max(x)
    else:
        return list(x.unique())
