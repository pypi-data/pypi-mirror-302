import os

# Root and Base Directories
CONFIG_DIR_PATH = os.path.join("./src/mlinvitrotox/config")
DATA_DIR_PATH = os.path.join("./data")
INPUT_DIR_PATH = os.path.join(DATA_DIR_PATH, "input")
OUTPUT_DIR_PATH = os.path.join(DATA_DIR_PATH, "processed")
RESULTS_DIR_PATH = os.path.join(DATA_DIR_PATH, "results")

# IDs
CHEM_ID = "DTXSID"
MASSBANK_ID = "GUID"
SMILES_ID = "SMILES"
SIRIUS_ID = "sirius_id"

# Data processing

# Step 1 input
MASSBANK_INPUT_DIR_PATH = os.path.join(INPUT_DIR_PATH, "hrms_massbank")
MASSBANK_INPUT_DIR_FOLDER = "published"
MASSBANK_UNIQUE_GUID = "massbank_unique_guids.csv"
SIRIUS_INPUT_DIR_PATH = os.path.join(INPUT_DIR_PATH, "sirius")
SIRIUS_TRAINING_STRUCTURES_INCHI = "sirius_training_structures_positive-mode_inchi.tsv"
SIRIUS_TRAINING_STRUCTURES_INCHI_DTXSID = (
    "sirius_training_structures_positive-mode_inchi_dtxsid.csv"
)

# Step 1 output
MASSBANK_OUTPUT_DIR_PATH = os.path.join(OUTPUT_DIR_PATH, "hrms_massbank")
EXTRACTED_MASSBANK_SUMMARY_SMILES = "massbank_published-data_smiles.csv"
EXTRACTED_MASSBANK_SUMMARY_COMPLETE = "massbank_published-data_complete.csv"
EXTRACTED_MASSBANK_GUID_DTXSID = "massbank_GUID-DTXSID.csv"


# Step 2 input
INVITRO_INPUT_DIR_PATH = os.path.join(INPUT_DIR_PATH, "invitro")
INVITRODB_CHEMICAL_LIST = "Chemical_List_ToxCast_invitroDB_v4_1-2024-04-29.csv"
SIRIUS_FPS_DEFINITIONS = "csi_fingerid.tsv"

# Step 2 output
FPS_OUTPUT_DIR_PATH = os.path.join(OUTPUT_DIR_PATH, "chemical_fingerprints")
INTERMEDIATE_FPS_OUTPUT_DIR_PATH = os.path.join(FPS_OUTPUT_DIR_PATH, "intermediate")
TRUE_FPS_TRAINING = "training_true-fps.parquet"
TRUE_FPS_VALIDATION = "validation_true-fps.parquet"


# Step 3 input
SIRIUS_MASSBANK_VALIDATION_DIR_FOLDER = "massbank_toxicity_5o8_eawag_sept2023_all"
SIRIUS_APPLICATION_DIR_FOLDER = "sources_fractions"

# Step 3 output
PRED_FPS_VALIDATION = "validation_sirius-pred-fps.parquet"
PRED_FPS_APPLICATION = "application_sirius-pred-fps.parquet"


# Step 4 input
# < no new input files >

# Step 4 output
VALIDATION_FPS_OUTPUT_DIR_PATH = os.path.join(FPS_OUTPUT_DIR_PATH, "validation")
VALIDATION_SELECTED_ABSINDEX = "massbank_validation_selected_absindex.csv"
VALIDATION_PRED_FPS_DTXSID = "massbank_validation_predfps_dtxsid.csv"


# Modeling

# Modeling input
CONFIG_FILE = "config.yaml"
CONFIG_MODELS_FILE = "config_classification.yaml"
PYTCPL_INPUT_FOLDER = "pytcpl"

# !! specify the relative path of your pytcpl repository here
REMOTE_DATA_DIR_PATH = os.path.join("../../pytcpl/data/")
REMOTE_PYTCPL_FOLDER = "output_final/"

ICE_REFERENCES = "ice_reference_file_mechtargets_aeid.csv"
PYTCPL_OVERVIEW_FILE = "assay_overview_selected.csv"

# Modeling output
MODELS_RESULTS_DIR_PATH = os.path.join(RESULTS_DIR_PATH, "models")
SELECTED_AEIDS = "selected_aeids.csv"
SELECTED_CHEMICALS = "selected_chemicals.csv"
