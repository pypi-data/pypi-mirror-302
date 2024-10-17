import os
import sys

from pathlib import Path

import pandas as pd

import mlinvitrotox.utils.extract_hrms_massbank_data as extract_mbd
import mlinvitrotox.utils.get_true_fps as get_truefps
import mlinvitrotox.utils.get_predicted_fps as get_predfps
import mlinvitrotox.utils.validate_massbank as validate
import mlinvitrotox.utils.training as ml

from mlinvitrotox.constants import (
    # IDs
    CHEM_ID,
    MASSBANK_ID,
    SMILES_ID,
    # Paths
    MASSBANK_INPUT_DIR_PATH,
    SIRIUS_INPUT_DIR_PATH,
    INVITRO_INPUT_DIR_PATH,
    MASSBANK_OUTPUT_DIR_PATH,
    FPS_OUTPUT_DIR_PATH,
    INTERMEDIATE_FPS_OUTPUT_DIR_PATH,
    VALIDATION_FPS_OUTPUT_DIR_PATH,
    # Folders
    MASSBANK_INPUT_DIR_FOLDER,  # 1
    SIRIUS_MASSBANK_VALIDATION_DIR_FOLDER,  # 5
    SIRIUS_APPLICATION_DIR_FOLDER,  # 6
    # Files
    MASSBANK_UNIQUE_GUID,  # 0
    SIRIUS_TRAINING_STRUCTURES_INCHI_DTXSID,  # 2
    EXTRACTED_MASSBANK_GUID_DTXSID,  # 10
    EXTRACTED_MASSBANK_SUMMARY_SMILES,  # 11
    EXTRACTED_MASSBANK_SUMMARY_COMPLETE,  # 12
    SIRIUS_FPS_DEFINITIONS,  # 3
    INVITRODB_CHEMICAL_LIST,  # 4
    TRUE_FPS_TRAINING,  # 13
    TRUE_FPS_VALIDATION,  # 14
    PRED_FPS_VALIDATION,  # 15
    PRED_FPS_APPLICATION,  # 16
    VALIDATION_SELECTED_ABSINDEX,  # 21
    VALIDATION_PRED_FPS_DTXSID,  # 20
)

# set input and output directories
massbank_input_directory = Path(MASSBANK_INPUT_DIR_PATH)
sirius_input_directory = Path(SIRIUS_INPUT_DIR_PATH)
invitro_input_directory = Path(INVITRO_INPUT_DIR_PATH)
massbank_output_directory = Path(MASSBANK_OUTPUT_DIR_PATH)
fps_output_directory = Path(FPS_OUTPUT_DIR_PATH)
intermediate_fps_output_directory = Path(INTERMEDIATE_FPS_OUTPUT_DIR_PATH)
validation_fps_output_directory = Path(VALIDATION_FPS_OUTPUT_DIR_PATH)


# * Extract and process MassBank HRMS data

# process MassBank input files
massbank_input_folder = massbank_input_directory / MASSBANK_INPUT_DIR_FOLDER
result_df = extract_mbd.process_files(massbank_input_folder)

# load SIRIUS training file with INCHIs and DTXSIDs
sirius_training_file = sirius_input_directory / SIRIUS_TRAINING_STRUCTURES_INCHI_DTXSID
df_sirius_training = pd.read_csv(sirius_training_file)
df_sirius_training = df_sirius_training.loc[
    df_sirius_training[CHEM_ID].notna(), [CHEM_ID]
]

# prepare GUIDs
# (this code only needs to be run once)
massbank_unique_guid_path = massbank_input_directory / MASSBANK_UNIQUE_GUID
create_unique_guids = False
if create_unique_guids:
    n_files = 20000
    extract_mbd.create_and_store_unique_guids(massbank_unique_guid_path, n_files)

# load unique guids
df_guid = pd.read_csv(massbank_unique_guid_path)

# set file paths for output files
# massbank summary grouped by SMILES
output_file_structures_validation = (
    massbank_output_directory / EXTRACTED_MASSBANK_SUMMARY_SMILES
)
# complete massbank summary by ACCESSION
output_file_extracted_massbank = (
    massbank_output_directory / EXTRACTED_MASSBANK_SUMMARY_COMPLETE
)
# file to match GUID and DTXSID
output_file_guid_dtxsid = massbank_output_directory / EXTRACTED_MASSBANK_GUID_DTXSID

# filter data
extract_mbd.filter_data(
    result_df,
    df_sirius_training,
    df_guid,
    output_file_structures_validation,
    output_file_extracted_massbank,
    output_file_guid_dtxsid,
)

# * Get true fingerprints for training and validation molecules

# read fingerprint definitions
sirius_fps_df_path = sirius_input_directory / SIRIUS_FPS_DEFINITIONS
df_csi = pd.read_csv(sirius_fps_df_path, sep="\t")

for step in ["TRAINING", "VALIDATION"]:
    print(step)

    # set id for chemical, and input and output paths
    if step == "TRAINING":
        # id
        id = CHEM_ID

        # input
        fps_input_file = INVITRODB_CHEMICAL_LIST
        fps_input_path = invitro_input_directory / fps_input_file

        # output
        fps_output_path = fps_output_directory / TRUE_FPS_TRAINING

    elif step == "VALIDATION":
        # id
        id = MASSBANK_ID

        # input
        fps_input_file = EXTRACTED_MASSBANK_SUMMARY_SMILES
        fps_input_path = massbank_output_directory / fps_input_file

        # output
        fps_output_path = fps_output_directory / TRUE_FPS_VALIDATION

    else:
        print("Please specify a valid step.")

    # set sdf and csv output path
    base_file_name = os.path.splitext(fps_input_file)[0]
    sdf_output_path = os.path.join(
        intermediate_fps_output_directory, f"{base_file_name}_clean.sdf"
    )
    csv_output_path = os.path.join(
        intermediate_fps_output_directory, f"{base_file_name}_clean.csv"
    )

    # process molecules
    smiles = SMILES_ID
    get_truefps.process_molecules(
        id,
        smiles,
        fps_input_path,
        df_csi,
        fps_output_path,
        csv_output_path,
        sdf_output_path,
    )


# * Process validation and application output from SIRIUS

# set input and output paths
for step in ["VALIDATION", "APPLICATION"]:
    if step == "VALIDATION":
        # input
        sirius_input_folder = (
            sirius_input_directory / SIRIUS_MASSBANK_VALIDATION_DIR_FOLDER
        )
        # complete massbank summary
        massbank_validation_input_file = (
            massbank_output_directory / EXTRACTED_MASSBANK_SUMMARY_COMPLETE
        )

        # output
        predfps_output_file = PRED_FPS_VALIDATION

    elif step == "APPLICATION":
        # input
        sirius_input_folder = sirius_input_directory / SIRIUS_APPLICATION_DIR_FOLDER
        # no massbank validation
        massbank_validation_input_file = None

        # output
        predfps_output_file = PRED_FPS_APPLICATION

    else:
        print("Please specify a valid step.")

    print("SIRIUS input folder (fpt files):", sirius_input_folder)

    # load true training fingerprints
    training_fps_input_path = fps_output_directory / TRUE_FPS_TRAINING
    df_truefps = ml.get_fingerprint_df(training_fps_input_path)

    # set path for output file
    predfps_output_path = fps_output_directory / predfps_output_file

    # check SIRIUS version
    matching_sirius_version = get_predfps.check_sirius_version(
        sirius_input_folder / SIRIUS_FPS_DEFINITIONS
    )
    if not matching_sirius_version:
        "Error: This data cannot be processed."
        sys.exit()

    # read SIRIUS .fpt files
    df_predfps = get_predfps.read_fps_files(
        sirius_input_folder,
        df_csi,
        threshold=0.5,
    )
    print(df_predfps.shape)
    print(df_predfps.columns)
    print(df_predfps)

    # only keep fingerprints bits used for training
    df_predfps_selected = get_predfps.keep_selected_fps_bits(
        df_predfps,
        df_truefps,
    )
    print(df_predfps_selected.shape)
    print(df_predfps_selected.columns)
    print(df_predfps_selected)

    # apply filtering and grouping (only relevant for MassBank validation data)
    if step == "VALIDATION":
        df_predfps_filtered = get_predfps.filter_mbval_data_by_accession(
            df_predfps_selected,
            massbank_validation_input_file,
        )
        # aggregate MassBank validation data
        df_predfps_grouped = df_predfps_filtered.groupby(MASSBANK_ID).agg(
            get_predfps.custom_agg
        )
        df_predfps_grouped["ACCESSION"] = df_predfps_grouped["ACCESSION"].apply(
            lambda x: sorted(x)
        )
        # drop columns
        columns_to_drop = [
            "sirius_id",
            "sirius_run",
            "formula",
            "adduct",
            "adjusted_sirius_run",
        ]
        df_predfps_grouped = df_predfps_grouped.drop(columns=columns_to_drop)
        df_predfps_final = df_predfps_grouped.copy()
        df_predfps_final = df_predfps_final.sort_index().reset_index()
    elif step == "APPLICATION":
        # remove "features" column for application data from PARC
        # TODO check if needed?
        # if SIRIUS_APPLICATION_DIR_FOLDER in ["sources_fractions"]:
        # df_predfps_selected = df_predfps_selected.drop(columns="features")
        df_predfps_final = df_predfps_selected.copy()

    print(
        f"The shape of the final data frame for step {step} with predicted fingerprints is: {df_predfps_final.shape}"
    )

    # store output
    df_predfps_final.to_parquet(predfps_output_path, index=False)


# * Perform SIRIUS validation

# Load MassBank validation dataframes
input_true_fps_validation = fps_output_directory / TRUE_FPS_VALIDATION
input_pred_fps_validation = fps_output_directory / PRED_FPS_VALIDATION
df_mbval_true_fps = validate.load_massbank_val_df(input_true_fps_validation)
df_mbval_pred_fps = validate.load_massbank_val_df(input_pred_fps_validation)

# process and drop columns
if "sirius_id" in df_mbval_pred_fps.columns:
    df_mbval_pred_fps["sirius_id"] = df_mbval_pred_fps["sirius_id"].astype("int")
df_mbval_pred_fps = df_mbval_pred_fps.drop(
    columns=["features", "TopCSIScore", "ACCESSION"]
)

# Filter dataframes to only contain shared chemicals (GUIDs)
(df_mbval_true_fps_filtered, df_mbval_pred_fps_filtered) = validate.filter_mbval_dfs(
    df_mbval_true_fps, df_mbval_pred_fps
)

# Calculate metrics per fingerprint bit
output_metrics_bit = (
    validation_fps_output_directory / "massbank_validation_metrics_absindex.csv"
)
df_metrics_bit = validate.calculate_metrics_per_bit(
    df_mbval_true_fps_filtered, df_mbval_pred_fps_filtered, output_metrics_bit
)

# Only keep fingerprint bits which were fit well enough
threshold_recall = 0.75
threshold_precision = 0.75
output_file = validation_fps_output_directory / VALIDATION_SELECTED_ABSINDEX
validate.save_indexes_passed_validation(
    df_metrics_bit, threshold_recall, threshold_precision, output_file
)

# Check if the MASSBANK_ID columns are the same in both dataframes
columns_are_same = (
    df_mbval_true_fps_filtered.index.sort_values()
    == df_mbval_pred_fps[MASSBANK_ID].sort_values().reset_index(drop=True)
).all()
print(f"MASSBANK_ID columns are the same: {columns_are_same}")
duplicates_true_fps = df_mbval_true_fps_filtered.duplicated().sum()
duplicates_pred_fps = df_mbval_pred_fps.set_index(MASSBANK_ID).duplicated().sum()
print(f"Number of duplicate rows in df_mbval_true_fps_filtered: {duplicates_true_fps}")
print(f"Number of duplicate rows in df_mbval_pred_fps: {duplicates_pred_fps}")

# read the GUID_DTXSID massbank summary file to filter on
input_GUID_DTXSID = massbank_output_directory / EXTRACTED_MASSBANK_GUID_DTXSID
df_guid_dtxsid = pd.read_csv(input_GUID_DTXSID)

# merge the pred fingerprints with DTXSID from the massbank summary file
# (this adds a few entries as some GUIDs have several DTXSIDs)
df_mbval_pred_fps_relevant = pd.merge(
    df_mbval_pred_fps,
    df_guid_dtxsid,
    left_on=MASSBANK_ID,
    right_on=MASSBANK_ID,
    how="inner",
)

# sort columns
list_cols = sorted(df_mbval_pred_fps_relevant.columns)
list_cols = [CHEM_ID, MASSBANK_ID] + [
    c for c in list_cols if c not in [CHEM_ID, MASSBANK_ID]
]
df_mbval_pred_fps_relevant = df_mbval_pred_fps_relevant[list_cols]

# calculate duplicated DTXSIDs
n_duplicated_dtxsid = df_mbval_pred_fps_relevant.duplicated(subset=[CHEM_ID]).sum()
print(f"Number of duplicated DTXSIDs: {n_duplicated_dtxsid}")

# for each duplicated DTXSID, we set a bit to 1 if it is active for one of the duplicates
aggregated_df = df_mbval_pred_fps_relevant.groupby(CHEM_ID).agg("max")

if MASSBANK_ID in aggregated_df.columns:
    aggregated_df = aggregated_df.drop(columns=MASSBANK_ID)
aggregated_df = aggregated_df.reset_index()
print(f"Shape of aggregated dataframe: {aggregated_df.shape}")
print(f"Columns of aggregated dataframe: {aggregated_df.columns}")

# print to file to be used as reference for ML
output_file = massbank_output_directory / VALIDATION_PRED_FPS_DTXSID
aggregated_df.sort_values(CHEM_ID).to_csv(output_file, index=False)
