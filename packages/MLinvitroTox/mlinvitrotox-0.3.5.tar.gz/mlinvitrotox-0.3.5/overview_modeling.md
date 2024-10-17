# MLinvitroTox modeling

The input data has been created in the data processing script.

Scripts: 
- `src/mlinvitrotox/train/trainmodels.py`
- `src/mlinvitrotox/train/evaluatemodels.py`
- `src/mlinvitrotox/train/providemodels.py`

The directory structure and the correspondings paths are organized and specified in `src/mlinvitrotox/constants.py`.


## Introduction

We fit each assay endpoint separately. They are provided as parquet or csv files where the filename corresponds to the assay endpoint id (aeid). In pytcpl, assay endpoints with less than 50 chemicals were filtered out. In subsequent steps, assay endpoints can be summarized to mechanistic target or similar depending on the research question.


## Train models

### Code:
- `src/mlinvitrotox/utils/training.py`

### Input:

#### Configuration files

2 configuration files, one for the pipeline in general, the other for the models to specify the hyperparameter grid for cross-validation

C. `src/mlinvitrotox/config/config.yaml`

C. `src/mlinvitrotox/config/config_classification.yaml`

#### pytcpl output for each aeid

Parquet files from pytcpl, one for each assay endpoint (in .gitignore, can be accessed through the pytcpl repository)

7. pytcpl files

parquet files: remote directory

parquet files: copied to `data/input/invitro/pytcpl` 


#### pytcpl overview file

To filter aeids and to have information on the signal direction of the mechanistic target

8. `data/input/invitro/assay_overview_selected.csv`

#### ICE references

The ICE references data contains information on the mechanistic targets of each assay endpoint. 

@Kasia: data source

9. `data/input/invitro/ice_reference_file_mechtargets_aeid.csv`

@Kasia: data source

#### True fingerprints by DTXSID

The true fingerprints are used as clustering input.

13. `data/processed/chemical_fingerprints/training_true-fps.parquet`

#### Mappings from chemicals (as DTXSIDs) to AbsoluteIndexes

Used to split into training, validation_true and validation_pred

20. `data/processed/chemical_fingerprints/hrms_massbank/massbank_true-vs-pred-fingerprint_mappings.csv`

#### AbsoluteIndexes passed validation

This files stores the stores the AbsoluteIndexes from the SIRIUS fingerprint that were fitted with good enough recall and precision in the data processing.

21. `data/processed/chemical_fingerprints/validation/massbank_validation_selected_absindex.csv`

If the config flag "sirius_quality_filtering" is set to 1, only the selected SIRIUS fingerprints bits with a high enough recall and precision are used for modelling


### Output:

#### Filtered assay endpoints (list of selected aeids)

30. `data/results/models_logs/<targetrun>/selected_aeids.csv`


#### Modeling log

All the modeling output are stored in the models folder. (in .gitignore)

31. `data/results/models/<targetrun>/`


## Modeling predictions (in 03)

### Code:
- `src/mlinvitrotox/utils/predict.py`

### Input

#### Modeling log

31. `data/results/models/<targetrun>/`

#### True training fingerprints

13. `data/processed/chemical_fingerprints/training_true-fps.parquet`


#### Predicted application fingerprints

16. `data/processed/chemical_fingerprints/application_sirius_pred-fps.parquet`


### Output

#### Modeling metrics

Metrics per aeid

33a. `data/results/models/modeltraining_metrics.csv`

#### Modeling predictions

Predictions for each chemical

33b. `data/results/models/modeltraining_predictions.csv`
