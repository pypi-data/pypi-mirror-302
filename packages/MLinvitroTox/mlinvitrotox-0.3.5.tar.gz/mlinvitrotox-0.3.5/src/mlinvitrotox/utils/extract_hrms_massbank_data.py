# Data processing: 1) extract and filter massbank data

import os
import re

from pathlib import Path

import pandas as pd
import numpy as np

import time

from mlinvitrotox.constants import (
    # IDs
    CHEM_ID,
    MASSBANK_ID,
    SMILES_ID,
)


def create_and_store_unique_guids(file_path, n_files):
    """
    create and store unique (and reproducible) IDs for the MassBank data

    """

    import random
    import uuid

    rd = random.Random()
    rd.seed(0)
    list_guids = [uuid.UUID(int=rd.getrandbits(128), version=4) for _ in range(n_files)]
    df_guid = pd.DataFrame(list_guids, columns=[MASSBANK_ID])
    df_guid.to_csv(file_path, index=False)


def read_and_extract_data(file_path, selected_keys):
    """
    helper function to read MassBank files and extract relevant information


    """

    # Open file
    with open(file_path, "r") as file:
        content = file.readlines()

    # Create a dictionary to store key-value pairs with unique keys
    key_value_dict = {}
    key_count = {}

    for line in content:
        # Use regular expression to extract key-value pairs
        match = re.match(r"([^:]+):\s*([^\n]+)", line)
        if match:
            key, value = match.groups()
            # Append a unique identifier to the key
            key_identifier = key_count.get(key, 0)
            key_count[key] = key_identifier + 1
            key = f"{key}_{key_identifier:02d}"
            if key in key_value_dict:
                key_value_dict[key] += f",{value.strip()}"
            else:
                key_value_dict[key] = value.strip()

    # Filter for rows containing selected keys
    key_value_dict_selected = {
        k: v
        for k, v in key_value_dict.items()
        if any(selected_key in k for selected_key in selected_keys)
    }

    return key_value_dict_selected


def process_files(input_directory, max_files=None):
    """
    function to process all MassBank txt files and compile them in a data frame


    """

    # Set relevant keys
    selected_keys = [
        "ACCESSION",
        "RECORD_TITLE",
        "CH$NAME",
        "CH$FORMULA",
        "CH$EXACT_MASS",
        "CH$SMILES",
        "CH$IUPAC",
        "CH$LINK",
        "AC$INSTRUMENT",
        "AC$MASS_SPECTROMETRY",
        "AC$CHROMATOGRAPHY",
        "MS$FOCUSED_ION",
    ]

    # initialize
    data_list = []

    # Get all text files in the input directory
    all_files = [f for f in os.listdir(input_directory) if f.endswith(".txt")]

    # Limit the number of files to process
    if max_files is not None:
        total_files = min(len(all_files), max_files)
    else:
        total_files = len(all_files)

    # Iterate over each text file in the input directory up to the limit
    for file_number, file_name in enumerate(all_files[:total_files], start=1):
        file_path = Path(input_directory) / file_name

        # Print progress
        print(f"Processing file {file_number} of {total_files}: {file_name}")

        # Extract key-value pairs for selected keys from the file
        key_value_dict = read_and_extract_data(file_path, selected_keys)

        # Append the result to the list
        data_list.append(key_value_dict)

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data_list)

    # Set base columns
    base_columns = [
        "CH$LINK",
        "MS$DATA_PROCESSING",
        "CH$NAME",
        "AC$INSTRUMENT",
        "AC$MASS_SPECTROMETRY",
        "MS$FOCUSED_ION",
        "AC$CHROMATOGRAPHY",
    ]

    # Process base columns
    for base_column in base_columns:
        # get corresponding full keys
        base_keys = [key for key in df.columns if key.startswith(base_column)]

        # join entries for each bsae column
        df[base_column] = df[base_keys].apply(
            lambda row: ",".join(row.dropna()), axis=1
        )

        # drop initial columns
        df = df.drop(columns=base_keys)

    return df


def filter_data(
    result_df,
    sirius_training_df,
    df_guid,
    output_file_structures_validation,
    output_file_extracted_massbank,
    output_file_guid_dtxsid,
):
    """
    function to filter MassBank dataframe

    """

    t0 = time.perf_counter()

    # replace some string parts
    result_df.columns = result_df.columns.str.replace("_00", "")

    # extract parts of some strings from CH$LINK
    link_extract = result_df["CH$LINK"].str.extract(
        r"CAS (?P<CAS>[^,]+)?,?"
        r".*?PUBCHEM CID:(?P<PUBCHEM>[^,]+)?,?"
        r".*?INCHIKEY (?P<INCHIKEY>[^,]+)?,?"
        r".*?CHEMSPIDER (?P<CHEMSPIDER>[^,]+)?"
        # r".*?COMPTOX (?P<COMPTOX>[^,]+)?"
    )

    # extract parts of some strings from AC$MASS_SPECTROMETRY
    # TODO try again to reduce filtering time
    # (split in two parts to reduce execution time from 8 minutes to 1 minute)
    mass_spectrometry_extract = result_df["AC$MASS_SPECTROMETRY"].str.extract(
        r"MS_TYPE (?P<MS_TYPE>[^,]+)?,?"
        r".*?ION_MODE (?P<ION_MODE>[^,]+)?,?"
        r".*?IONIZATION (?P<IONIZATION>[^,]+)?,?"
        r".*?FRAGMENTATION_MODE (?P<FRAGMENTATION_MODE>[^,]+)?,?"
        # )
        # mass_spectrometry_extract2 = result_df["AC$MASS_SPECTROMETRY"].str.extract(
        r".*?COLLISION_ENERGY (?P<COLLISION_ENERGY>[^,]+)?,?"
        r".*?RESOLUTION (?P<RESOLUTION>[^,]+)?,?"
        r".*?MASS_RANGE_M/Z (?P<MASS_RANGE_M_Z>[^,]+)?"
    )

    t1 = time.perf_counter()
    print(f"Extract and concatenate {t1 - t0:0.4f} seconds")

    # extract parts of some strings from MS$FOCUSED_ION
    focused_ion_extract = result_df["MS$FOCUSED_ION"].str.extract(
        r"BASE_PEAK (?P<BASE_PEAK>[^,]+)?,?"
        r".*?PRECURSOR_M/Z (?P<PRECURSOR_M_Z>[^,]+)?,?"
        r".*?PRECURSOR_TYPE (?P<PRECURSOR_TYPE>[^,]+)?"
    )

    # concatenate
    result_df = pd.concat(
        [result_df, link_extract, mass_spectrometry_extract, focused_ion_extract],
        axis=1,
        # [result_df, link_extract, mass_spectrometry_extract, mass_spectrometry_extract2, focused_ion_extract], axis=1
    )

    # extract DTXSID
    result_df[CHEM_ID] = result_df["CH$LINK"].str.extract(r"(DTXSID\d+)")

    # drop some columns
    result_df = result_df.drop(
        columns=[
            "MS$DATA_PROCESSING",
            "MS$FOCUSED_ION",
            "AC$MASS_SPECTROMETRY",
            "CH$LINK",
        ]
    )

    # rename some columns
    result_df.columns = [col.replace("CH$", "") for col in result_df.columns]
    result_df.columns = [col.replace("AC$", "") for col in result_df.columns]

    # unify NAs
    result_df.replace(["N/A", "na", "-", " "], np.nan, inplace=True)

    # drop SMILES columns
    result_df.dropna(subset=[SMILES_ID], inplace=True)

    # only keep certain instrumental conditions
    instrumental_strings = ["ESI", "APCI", "APPI", "MALDI"]
    instrument_regex = "|".join(instrumental_strings)
    instrument_condition = result_df["INSTRUMENT"].str.contains(
        instrument_regex, case=False, na=False
    )
    gc_condition = result_df["INSTRUMENT"].str.contains("GC", case=False, na=False)
    filtered_df = result_df[instrument_condition & ~gc_condition]
    filtered_df = filtered_df.dropna(subset=[CHEM_ID])

    # add a column indicating the presence of SIRIUS training compounds
    filtered_df = filtered_df.copy()
    filtered_df.loc[:, "sirius_training"] = filtered_df[CHEM_ID].apply(
        lambda x: "unsafe" if x in sirius_training_df[CHEM_ID].values else "safe"
    )

    # get df with unique smiles
    unique_smiles_df = (
        filtered_df.groupby(SMILES_ID)["ACCESSION"].apply(list).reset_index()
    )
    unique_smiles_df = unique_smiles_df.rename(columns={"ACCESSION": "ACCESSION_LIST"})
    unique_smiles_df["ACCESSION_LIST"] = unique_smiles_df["ACCESSION_LIST"].apply(
        lambda x: sorted(x)
    )

    # assign GUID
    unique_smiles_df[MASSBANK_ID] = df_guid[MASSBANK_ID][
        : len(unique_smiles_df)
    ].to_list()

    # store MassBank output grouped by SMILES
    unique_smiles_df = unique_smiles_df.sort_values(SMILES_ID)
    unique_smiles_df.to_csv(output_file_structures_validation, index=False)

    # get entries per ACCESSION back
    tidy_smiles_df = unique_smiles_df.explode("ACCESSION_LIST")
    tidy_smiles_df = tidy_smiles_df.rename(columns={"ACCESSION_LIST": "ACCESSION"})

    # store complete MassBank output (by ACCESSION)
    tidy_smiles_subset = tidy_smiles_df[["ACCESSION", MASSBANK_ID]]
    merged_df = pd.merge(filtered_df, tidy_smiles_subset, on="ACCESSION", how="inner")
    merged_df = merged_df.sort_values("ACCESSION")
    merged_df.to_csv(output_file_extracted_massbank, index=False)

    # count duplicate ids
    massbank_ref_file = merged_df.dropna(subset=[CHEM_ID])
    massbank_ref_file = massbank_ref_file[[CHEM_ID, MASSBANK_ID]].drop_duplicates()
    count_chem_id_per_massbank = massbank_ref_file.groupby(MASSBANK_ID)[
        CHEM_ID
    ].nunique()
    multiple_chem_id_count = count_chem_id_per_massbank[
        count_chem_id_per_massbank > 1
    ].count()
    print(f"How many GUIDs in total? {massbank_ref_file[MASSBANK_ID].nunique()} ")
    print(f"How many GUIDs have multiple DTXSID? {multiple_chem_id_count} ")

    # store GUID DTXSID matching
    massbank_ref_file = massbank_ref_file.reset_index(drop=True)
    massbank_ref_guid_dtxsid_duplicates = massbank_ref_file.duplicated().sum()
    print(massbank_ref_guid_dtxsid_duplicates)
    massbank_ref_guid_dtxsid = massbank_ref_file.drop_duplicates()
    print(massbank_ref_guid_dtxsid[CHEM_ID].nunique())
    massbank_ref_guid_dtxsid = massbank_ref_guid_dtxsid.sort_values(CHEM_ID)
    massbank_ref_guid_dtxsid.to_csv(output_file_guid_dtxsid, index=False)
    print(massbank_ref_guid_dtxsid.shape)
