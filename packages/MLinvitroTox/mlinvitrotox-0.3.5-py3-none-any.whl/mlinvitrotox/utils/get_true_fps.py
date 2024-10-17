# Data processing: 2) get true fingerprints
import re

import warnings

import pandas as pd
import numpy as np
from tqdm import tqdm
import logging

from rdkit import Chem
from rdkit.Chem.MolStandardize import rdMolStandardize
from openbabel import pybel
from CDK_pywrapper import CDK, FPType


def remove_illegal_smiles(
        df, 
        col_smiles, 
        nonallowed,
    ):
    """
    Remove rows where SMILES string contains specific non-allowed strings or characters
    """
    nonallowed_pattern = "|".join(map(re.escape, nonallowed))
    mask = df[col_smiles].str.contains(nonallowed_pattern, na=False)
    df_clean = df[~mask]
    return df_clean


def _standardize_smiles(raw_smiles):
    """
    helper function to be used with pandas apply
    
    """
    if raw_smiles is None:
        return None
    try:
        # Standardize and desalt the molecule
        std1_smiles = rdMolStandardize.StandardizeSmiles(raw_smiles)
        desalter = rdMolStandardize.LargestFragmentChooser()
        desalt_mol = desalter.choose(Chem.MolFromSmiles(std1_smiles))
        std2_smiles = rdMolStandardize.StandardizeSmiles(Chem.MolToSmiles(desalt_mol))
        return std2_smiles
    except Exception as e:
        # Log the exception and return None
        logging.warning(f"Error processing molecule: {raw_smiles}; Error: {e}")
        return None


def process_molecules(
        id,
        smiles,
        fps_input_path,
        df_csi,
        fps_output_path,
        csv_output_path,
        sdf_output_path,
        store_as_csv=False,
):

    # Read the CSV data
    df_fps_input = pd.read_csv(fps_input_path)
    print(f"Dataframe with provided SMILES: {df_fps_input.shape[0]} entries")

    # Check for duplicates
    if df_fps_input[id].duplicated().any():
        warnings.warn(
            f"The file {fps_input_path} contains duplicates based on the column '{id}'"
        )

    # Keep SMILES and chemical ID
    cols_to_keep = [id, smiles]
    df = df_fps_input[cols_to_keep].copy()

    # pre-cleanup
    print("Dataframe cleaning...")
    df.loc[:, id] = df[id].str.replace(
        "https://comptox.epa.gov/dashboard/chemical/details/", ""
    )
    df = remove_illegal_smiles(df, smiles, ["Zn", "Pt", "<", ">", "R"])
    df = df[df[smiles].str.count("[Cc]") >= 2]
    df.loc[:, "sdf"] = df[smiles].apply(lambda x: Chem.MolFromSmiles(x) if x else None)
    df.dropna(subset=["sdf"], inplace=True)

    # standardize according to chemdbl procedure
    df["standardized_smiles"] = df[smiles].apply(_standardize_smiles)
    df["standardized_mol"] = df["standardized_smiles"].apply(
        lambda x: Chem.MolFromSmiles(x) if x else None
    )

    # Store sdf file
    writer = Chem.SDWriter(sdf_output_path)
    for index, row in df.sort_values(id).iterrows():
        mol = row["standardized_mol"]
        chem_id = row[id]
        if mol is not None:
            mol.SetProp(id, chem_id)
            writer.write(mol)
    writer.close()

    # Store csv file
    cols_to_save = [id, smiles, "standardized_smiles"]
    df[cols_to_save].sort_values(id).to_csv(csv_output_path, index=False)
    print(f"After cleaning: {df.shape[0]} entries")

    # generate FP3 and FP4 openbabel fingerprints via pybel
    list_mols_dtxsid = []
    for mol in pybel.readfile("sdf", str(sdf_output_path)):
        if mol is not None:
            # Try to retrieve the molecule_id, default to "Unknown" if not found
            try:
                dtxsid = (
                    mol.OBMol.GetData(id).GetValue()
                    if mol.OBMol.HasData(id)
                    else "Unknown"
                )
            except Exception:
                dtxsid = "Unknown"
            list_mols_dtxsid.append((dtxsid, mol))

    # FP3
    list_binary_vectors_fp3 = []
    n_bits = 55
    for dtxsid, mol in tqdm(list_mols_dtxsid, desc="Calculating FP3", unit="mol"):
        fp_bits_active = mol.calcfp(fptype="FP3").bits
        bv = np.zeros(n_bits, dtype=int)
        if fp_bits_active:
            fp_indexes = [i - 1 for i in fp_bits_active]
            bv[fp_indexes] = 1
        # Append the bits directly
        list_binary_vectors_fp3.append(
            {**{f"fp3_bit_{i+1}": bv[i] for i in range(n_bits)}, id: dtxsid}
        )

    df_binary_vectors_fp3 = pd.DataFrame(list_binary_vectors_fp3)
    df_binary_vectors_fp3 = df_binary_vectors_fp3.set_index(id)

    # FP4
    list_binary_vectors_fp4 = []
    n_bits = 307
    for dtxsid, mol in tqdm(list_mols_dtxsid, desc="Calculating FP4", unit="mol"):
        fp_bits_active = mol.calcfp(fptype="FP4").bits
        bv = np.zeros(n_bits, dtype=int)
        if fp_bits_active:
            fp_indexes = [i - 1 for i in fp_bits_active]
            bv[fp_indexes] = 1
        # Append the bits directly
        list_binary_vectors_fp4.append(
            {**{f"fp4_bit_{i+1}": bv[i] for i in range(n_bits)}, id: dtxsid}
        )

    df_binary_vectors_fp4 = pd.DataFrame(list_binary_vectors_fp4)
    df_binary_vectors_fp4 = df_binary_vectors_fp4.set_index(id)

    # concatenate FP3 and FP4
    df_obabel = pd.concat([df_binary_vectors_fp3, df_binary_vectors_fp4], axis=1)

    # create MACCS, PubChem and Klekota-Roth fingerprints with CKW_pywrapper
    list_mols = []
    list_chem_ids = []
    sdf_supplier = Chem.SDMolSupplier(sdf_output_path)

    for mol in tqdm(sdf_supplier, desc="Preparing for MACCS, PubChem and Klekota-Roth", unit="mol"):
        if mol is not None:
            list_mols.append(Chem.AddHs(mol))
            list_chem_ids.append(mol.GetProp(id))

    # calculate fingerprints
    print("Calculating MACCS, PubChem and Klekota-Roth fingerprints takes some time...")
    cdk = CDK(fingerprint=FPType.MACCSFP)
    df_maccs = cdk.calculate(list_mols, show_banner=False)
    cdk = CDK(fingerprint=FPType.PubchemFP)
    df_pubchem = cdk.calculate(list_mols, show_banner=False)
    cdk = CDK(fingerprint=FPType.KRFP)
    df_klekotaroth = cdk.calculate(list_mols, show_banner=False)

    # concatenate CDK fingerprints
    df_cdk = pd.concat((df_maccs, df_pubchem, df_klekotaroth), axis=1)
    df_cdk.index = list_chem_ids

    # concatenate CKD and pybel fingerprints
    df_fps = pd.concat((df_obabel, df_cdk), axis=1)
    print(f"FP3, FP4, MACCS, PubChem, Klekota-Roth: {df_fps.shape[1]} bits before overlap with SIRIUS bits")
    df_fps.columns = range(len(df_fps.columns))

    # get overlap with CSI FingerID absoluteIndex
    df_csi["absoluteIndex"] = df_csi["absoluteIndex"].astype(int)
    valid_indices = set(df_csi["absoluteIndex"]).intersection(set(df_fps.columns))
    df_fps_filtered = df_fps[list(valid_indices)]
    df_fps_filtered.columns = [str(col).zfill(4) for col in df_fps_filtered.columns]

    # Ranges of each fingerprint type (only informative)
    openbabel_fp3_range = range(0, 55)
    openbabel_fp4_range = range(55, 362)
    MACCS_range = range(369, 525)
    PubChem_range = range(659, 1395)
    klekota_range = range(1409, 6267)
    print_info = (
        "The absoluteIndex from csi_fingerid.tsv file "
        "is used as column names. The following fingerprints were generated:\n"
        f"openbabel_fp3 fingerprints (absoluteIndex range {openbabel_fp3_range.start} - {openbabel_fp3_range.stop - 1}),\n"
        f"openbabel_fp4 CDK Substructure in SIRIUS ({openbabel_fp4_range.start} - {openbabel_fp4_range.stop - 1}),\n"
        f"MACCS ({MACCS_range.start} - {MACCS_range.stop - 1}),\n"
        f"PubChem ({PubChem_range.start} - {PubChem_range.stop - 1}),\n"
        f"Klekota-Roth ({klekota_range.start} - {klekota_range.stop - 1})."
    )
    print(print_info)

    df_fps_filtered = df_fps_filtered.reset_index().rename(columns={"index": id})
    df_fps_filtered = df_fps_filtered.sort_values(id)
    if store_as_csv:
        df_fps_filtered.to_csv(fps_output_path, index=False)
    else:
        df_fps_filtered.to_parquet(fps_output_path, index=False)

    print(f"Final dataframe with {df_fps_filtered.shape[1]} true SIRIUS fingerprint bits for {df_fps_filtered.shape[0]} entries (stored as {fps_output_path})")
