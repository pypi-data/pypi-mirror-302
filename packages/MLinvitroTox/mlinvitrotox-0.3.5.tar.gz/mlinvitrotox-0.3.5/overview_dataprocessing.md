# MLinvitroTox data processing

In data processing, all input input data is prepared for modeling. 

The data is open source and provided by us. The only exception is the application in the `data/input/sirius/sources_fractions`.

Script: `src/mlinvitrotox/train/processinputdata.py`

The directory structure and the correspondings paths are organized and specified in `src/mlinvitrotox/constants.py`.

TODO load big data sets from external sources


## Step 0: Extract SIRIUS directories

The SIRIUS directories need to be extracted before they can be processed with MLinvitroTox. Run `src/mlinvitrotox/apply/extractsiriusdata path/to/siriusfolder`. This takes a few minutes, depending on the folder size.



## Step 1: Filter and extract MassBank data

### Code:
- `src/mlinvitrotox/utils/extract_hrms_massbank_data.py`

### Input:

#### MassBank files (open-access)

1. `data/input/hrms_massbank/published/` 

Source:  `https://zenodo.org/records/10213786` or `https://github.com/MassBank/MassBank-data`

The folder contains 100'026 files (462 MB) (27.03.2024). When new MassBank files become available, they need to be added to this folder and everything has to be reprocessed.

TODO load from external source (check whether we have latest state of files)

Note: We are using a version from Sept. 2023 plus Eawag spectra that have not yet been released. The eawag files habe been submitted in the meantime. 

These files (1) are processed with `process_files` and returned as a dataframe. In `filter_data`, the dataframe is filtered and SIRIUS training structures from file (2) are marked in the column `sirius_training` as `unsafe` if present in (2) or `safe` otherwise.

#### SIRIUS training structures (open-access)

2a. `data/input/sirius/sirius_training_structures_positive-mode_inchi.tsv`

The file is from `https://bio.informatik.uni-jena.de/software/sirius/`, section `Integration of CSI:FingerID`. We store the positive mode file and use it to assess which chemicals are "safe" to validate on. 

NEWSIRIUS check whether this file will be updated

NEWSIRIUS The pipeline (and the publication) is for the positive mode only. Later: negative mode

Using the INCHIKEYs from file (2a), the DTXSIDs were retrieved from `https://comptox.epa.gov/dashboard/batch-search` on April 23, 2024.

2b. `data/input/sirius/sirius_training_structures_positive-mode_inchi_dtxsid.csv`

#### Unique GUIDs

0. `data/input/hrms_massbank/massbank_unique_guids.csv`

This function needs to be run only once. It creates a file with 20,000 unique GUIDs for the MassBank data.


### Output:

#### MassBank summary grouped by SMILES

11. `data/processed/hrms_massbank/massbank_published-data_smiles.csv`

A file with the SMILES, ACCESSION_LIST and GUID, grouped by SMILES resulting in several ACCESSIONs per SMILES

#### MassBank summary complete

12. `data/processed/hrms_massbank/massbank_published-data_complete.csv`

The complete filtered massbank output with 1 entry per ACCESSION

#### File to match GUID and DTXSID

10. `data/processed/hrms_massbank/massbank_GUID-DTXSID.csv`



## Step 2: Get true fingerprints

These step is done twice, for training and validation.

### Code:
- `src/utils/get_true_fps.py`

### Input (for training):

#### CSI FingerID definitions

3. `data/input/sirius/csi_fingerid.tsv`

NEWSIRIUS this will likely change with the new SIRIUS version

#### List of chemicals

4. `data/input/invitro/Chemical_List_Toxcast_invitroDB_v4_1-2024-04-29.csv`

This file is downloaded from `https://comptox.epa.gov/dashboard/chemical-lists`.

### Input (for validation):

#### CSI FingerID definitions

3. `data/input/sirius/csi_fingerid.tsv`

#### SMILES from summarized MassBank data

11. `data/processed/hrms_massbank/massbank_published-data_smiles.csv`

This is an output from step 1.


### Output (for training):

#### True fingerprints by DTXSID

13. `data/processed/chemical_fingerprints/training_true-fps.parquet`

#### Intermediate sdf file

This file is not needed later on but we keep it to check whether the rdkit package version has an impact.

xx. `data/processed/chemical_fingerprints/intermediate/Chemical_List_ToxCast_invitroDB_v3_5-2023-07-07_clean.sdf`

#### File with DTXSID, SMILES, standardized_smiles

xx. `data/processed/chemical_fingerprints/intermediate/Chemical_List_ToxCast_invitroDB_v3_5-2023-07-07_clean.csv`


### Output (for validation):

#### True fingerprints by GUID

14. `data/processed/chemical_fingerprints/validation_true-fps.parquet`

#### Intermediate sdf file

This file is not needed later on but we keep it to check whether the rdkit package version has an impact.

xx. `data/processed/chemical_fingerprints/intermediate/massbank_published-data_smiles_clean.sdf`

#### File with DTXSID, SMILES, standardized_smiles

xx. `data/processed/chemical_fingerprints/intermediate/massbank_published-data_smiles_clean.csv`

NEWSIRIUS dependence on fingerprints: which fingerprints? which lengths?



## Step 3: Get predicted fingerprints from SIRIUS

These step is done twice, for validation and testing.

### Code:
`src/utils/get_predicted_fps.py`

#### Input (for validation):

3. `data/input/sirius/csi_fingerid.tsv`

5. `data/input/sirius/massbank_toxicity_5o8_eawag_sept2023_all`

SIRIUS output for the MassBank files. They need to be unzipped.

TODO provide with a link

TODO these files are currently in gitignore

12. `data/processed/hrms_massbank/massbank_published-data_complete.csv`

Output from step 1

13. `data/processed/chemical_fingerprints/training_true-fps.parquet`

Output from Step 2

### Input (for application): 

3. `data/input/sirius/csi_fingerid.tsv`

6. `data/input/sirius/sources_fractions` (not open-access)

SIRIUS output for PARC files. They need to be unzipped.

!!! This files are not open-access !!!

TODO unzip

TODO this files are currently in gitignore

13. `data/processed/chemical_fingerprints/training_true-fps.parquet`

Output from Step 2

### Output (for validation):

15. `data/processed/chemical_fingerprints/validation_sirius_pred-fps.parquet`

### Output (for application):

16. `data/input/processed/chemical_fingerprints/application_sirius_pred-fps.parquet`



## Step 4: MassBank validation of SIRIUS

### Code:
`src/utils/validate_massbank.py`

### Input:

14. `data/processed/chemical_fingerprints/validation_true-fps.parquet`

Output from Step 2

15. `data/processed/chemical_fingerprints/validation_sirius_pred-fps.parquet`

Output from Step 3

10. `data/hrms_massbank/massbank_GUID-DTXSID.csv`

Output from Step 1

### Output:

#### Validation metrics per fingerprint bit

xx. `data/processed/chemical_fingerprints/validation/massbank_validation_metrics_absindex.csv`

#### Some mappings from chemicals (as DTXSIDs) to AbsoluteIndexes

20. `data/processed/chemical_fingerprints/hrms_massbank/massbank_validation_predfps_dtxsid.csv`

#### AbsoluteIndexes passed validation

Only keep fingerprint bits with good enough recall and precision

21. `data/processed/chemical_fingerprints/validation/massbank_validation_selected_absindex.csv`
