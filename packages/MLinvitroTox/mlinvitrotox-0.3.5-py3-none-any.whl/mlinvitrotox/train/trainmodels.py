import shutil

from pathlib import Path

import pandas as pd
import numpy as np
from datetime import datetime
import traceback

import mlinvitrotox.utils.training as ml

from mlinvitrotox.constants import (
    # Paths
    REMOTE_DATA_DIR_PATH,
    INVITRO_INPUT_DIR_PATH,
    CONFIG_DIR_PATH,
    FPS_OUTPUT_DIR_PATH,
    VALIDATION_FPS_OUTPUT_DIR_PATH,
    MASSBANK_OUTPUT_DIR_PATH,
    MODELS_RESULTS_DIR_PATH,  # 31
    # Folders
    REMOTE_PYTCPL_FOLDER,  # 7
    PYTCPL_INPUT_FOLDER,  # 7
    # Files
    SELECTED_AEIDS,  # 30
    SELECTED_CHEMICALS,  # part of 31
    PYTCPL_OVERVIEW_FILE,  # 8
    ICE_REFERENCES,  # 9
    CONFIG_FILE,  # C
    CONFIG_MODELS_FILE,  # C
    TRUE_FPS_TRAINING,  # 13
    VALIDATION_PRED_FPS_DTXSID,  # 20
    VALIDATION_SELECTED_ABSINDEX,  # 21
)

# !! in config_classiffication, use complete hyperparameter grid again

# Get pytcpl output from remote repository
remote_pytcpl_folder = Path(REMOTE_DATA_DIR_PATH) / REMOTE_PYTCPL_FOLDER
pytcpl_input_folder = Path(INVITRO_INPUT_DIR_PATH) / PYTCPL_INPUT_FOLDER
if 1:
    if pytcpl_input_folder.is_dir():
        ml.empty_pytcpl_input_directory(pytcpl_input_folder)
    else:
        pytcpl_input_folder.mkdir(parents=True, exist_ok=True)

    if remote_pytcpl_folder.is_dir():
        ml.copy_pytcpl_parquet_files(remote_pytcpl_folder, pytcpl_input_folder)
    else:
        print("Provide a valid remote pytpcl folder in constants.py")

# Set main folder to log results
logs_folder = Path(MODELS_RESULTS_DIR_PATH)

# Get ML configuration
config_path = Path(CONFIG_DIR_PATH) / CONFIG_FILE
config_models_path = Path(CONFIG_DIR_PATH) / CONFIG_MODELS_FILE
CONFIG, _, LOGGER, RUN_FOLDER, LOG_PATH = ml.load_config(config_path, logs_folder)

# set some configuration values
target_variable = CONFIG["target_variable"]
TARGET_VARIABLE = ml.init_target_variable(target_variable)
ml_algorithm = "classification"
CONFIG_ESTIMATORS = ml.init_ml_algo(ml_algorithm, str(config_models_path))

# load ICE references file and pytcpl overview file
ice_input_file = Path(INVITRO_INPUT_DIR_PATH) / ICE_REFERENCES
ice_df = pd.read_csv(ice_input_file)
pytcpl_overview_file = Path(INVITRO_INPUT_DIR_PATH) / PYTCPL_OVERVIEW_FILE
pytcpl_df = pd.read_csv(pytcpl_overview_file)
assay_info_df = ml.merge_assay_info(pytcpl_df, ice_df)

# load aeid files
aeid_info_df = ml.get_aeid_files(
    pytcpl_input_folder,
    target_variable,
    assay_info_df,
)

# Select aeids
available_aeid_list = aeid_info_df["aeid"].tolist()
available_aeid_list = [str(aeid) for aeid in sorted(available_aeid_list)]
aeid_list = ml.select_aeids_for_training(
    pytcpl_input_folder,
    aeid_info_df,
    aeids=available_aeid_list,
    #    mech_target="Androgen"    # A mechanistic target can be specified.
)
LOGGER.info(f"AEIDs selected for training: {aeid_list}")
LOGGER.info(f"Number of target aeids: {len(aeid_list)}")

# Get true fingerprint data (from training)
LOGGER.info("get_fingerprint_df function is running")
LOGGER.info("#" * 60)
fps_input_file = Path(FPS_OUTPUT_DIR_PATH) / TRUE_FPS_TRAINING
fps_df = ml.get_fingerprint_df(fps_input_file)

# Iterate through aeids_target_assays and launch each iteration in a separate process
selected_aeid_list = []
# !! use the complete list for model training
# for aeid in aeid_list:
# !! use a shorter list for working on the code
for aeid in aeid_list[:3]:
    # log mechanistic target and aenm
    mech_target = aeid_info_df[aeid_info_df["aeid"].astype(str) == aeid][
        "MechanisticTarget"
    ].iloc[0]
    acen = aeid_info_df[aeid_info_df["aeid"].astype(str) == aeid][
        "assay_component_endpoint_name"
    ].iloc[0]
    LOGGER.info(
        f"Included AEID: {aeid}, MechanisticTarget: {mech_target}, assay component endpoint name: {acen}"
    )

    try:
        # init aeid
        ml.init_aeid(aeid)
        LOGGER.info(
            f"Start ML pipeline for assay ID: {aeid} and target variable: {target_variable}"
        )
        LOGGER.info("#" * 60)
        # get toxicity data
        LOGGER.info("process_single_aeid function is running")
        LOGGER.info("#" * 60)
        ice_omit_filtering = CONFIG["apply"]["ice_omit_filtering"]
        activity_threshold = CONFIG["activity_threshold"]
        assay_df = ml.process_single_aeid(
            pytcpl_input_folder,
            aeid,
            target_variable,
            ice_omit_filtering,
            activity_threshold,
        )
        LOGGER.info(f"Activity threshold: >= {activity_threshold} is active \n")

        # merge chemical ids in both dataframes
        LOGGER.info("merge_assay_and_fingerprint_df function is running")
        LOGGER.info("#" * 60)
        selected_chemicals_file = SELECTED_CHEMICALS
        merged_df = ml.merge_assay_and_fingerprint_df(
            assay_df,
            fps_df,
            selected_chemicals_file,
        )
        merged_df[target_variable] = merged_df[target_variable].astype(int)
        # LOGGER.info(f" Columns in the df: {merged_df.columns}")
        LOGGER.info(f"Shape of the merged df: {merged_df.shape}")
        LOGGER.info(f"hitcall column type: {merged_df[target_variable].dtype}")

        # filter aeids with little data and few positive labels
        dtxsid_count = 100
        npos_count = 10
        if len(merged_df) < dtxsid_count:
            LOGGER.info(f"Less than {dtxsid_count} chemicals for aeid: {aeid}")
            LOGGER.info(f"Not used for modeling: {aeid}")
            continue
        if np.sum(merged_df[target_variable] == 1) < npos_count:
            LOGGER.info(f"Less than {npos_count} positive labels for aeid: {aeid}")
            LOGGER.info(f"Not used for modeling: {aeid}")
            continue
        LOGGER.info(f"Used for modeling: {aeid}")
        selected_aeid_list.append(aeid)

        # cluster molecules within hitcall groups
        LOGGER.info("clustering is running")
        LOGGER.info("#" * 60)
        n_cls_0 = CONFIG["apply"]["n_cls_0"]
        n_cls_1 = CONFIG["apply"]["n_cls_1"]
        random_state = CONFIG["random_state"]
        clust_df = ml.clustering(
            merged_df,
            target_variable,
            n_cls_0,
            n_cls_1,
            random_state,
        )
        LOGGER.info(f"Shape of the clustered dataframe: {clust_df.shape}")
        LOGGER.info(f"Counts of 0s and 1s: {clust_df[target_variable].value_counts()}")

        # filter for indexes with good validation performance
        sirius_quality_filtering = CONFIG["apply"]["sirius_quality_filtering"]
        if sirius_quality_filtering == 1:
            LOGGER.info("filter_with_sirius_quality_indexes function is running")
            LOGGER.info("#" * 60)
            indexes_path = (
                Path(VALIDATION_FPS_OUTPUT_DIR_PATH) / VALIDATION_SELECTED_ABSINDEX
            )
            filtered_df = ml.filter_with_sirius_quality_indexes(
                clust_df,
                indexes_path,
                target_variable,
            )
        else:
            filtered_df = clust_df.copy()
        LOGGER.info(f"Filtered dataframe shape: {filtered_df.shape}")

        # split data into training and validation data
        LOGGER.info("split_training_validation_data function is running")
        LOGGER.info("#" * 60)
        pred_fps_file = Path(MASSBANK_OUTPUT_DIR_PATH) / VALIDATION_PRED_FPS_DTXSID
        pred_fps_df = pd.read_csv(pred_fps_file)
        LOGGER.info(f"Data frame shape of pred_fps_dtxsid: {pred_fps_df.shape}")
        # LOGGER.info(f"Data frame columns in pred_fps_dtxsid: {pred_fps_df.columns}")
        (
            df_train_test,
            df_validation_true,
            df_validation_pred,
        ) = ml.split_training_validation_data(
            filtered_df,
            pred_fps_df,
            target_variable,
        )

        # Partition data into X and y and respective massbank validation set
        # (massbank validation set evaluates generalization to unseen spectral data)
        LOGGER.info("partition training and validation data is running")
        LOGGER.info("#" * 60)
        (X, y, cluster, feature_names) = ml.partition_training_data(
            df_train_test,
            target_variable,
        )

        (
            X_mbval_structure,
            X_mbval_sirius,
            y_mbval,
        ) = ml.partition_validation_data(
            df_validation_true, df_validation_pred, target_variable, feature_names
        )
        LOGGER.info(f"Training X shape: {X.shape}")
        LOGGER.info(f"X_mbval_structure shape: {X_mbval_structure.shape}")
        LOGGER.info(f"X_mbval_sirius: {X_mbval_sirius.shape}")
        if not X.columns.equals(X_mbval_structure.columns) or not X.columns.equals(
            X_mbval_sirius.columns
        ):
            LOGGER.warning(
                "Columns in X, X_mbval_structure, and X_mbval_sirius are not the same!"
            )

        # Split data into train test set
        # (Stratified split by clusters)
        # (Single member clusters are in the training set)
        LOGGER.info("split_training_data is running")
        LOGGER.info("#" * 60)
        train_test_split_ratio = CONFIG["train_test_split_ratio"]
        X_train, y_train, X_test, y_test = ml.split_training_data(
            X,
            y,
            cluster,
            train_test_split_ratio,
            random_state,
        )

        # Apply oversampling
        oversampling = CONFIG["apply"]["oversampling"]
        if oversampling == 1:
            LOGGER.info(" oversampling is running")
            LOGGER.info("#" * 60)
            X_train_os, y_train_os = ml.handle_oversampling(
                X_train,
                y_train,
                random_state,
            )
        else:
            X_train_os = X_train.copy()
            y_train_os = y_train.copy()

        # Prepare feature selection
        feature_selection = CONFIG["apply"]["feature_selection"]
        remove_lowvariance_features = CONFIG["apply"]["remove_lowvariance_features"]
        remove_highcorrelation_features = CONFIG["apply"][
            "remove_highcorrelation_features"
        ]
        variance_threshold = CONFIG["feature_selection"]["variance_threshold"]
        correlation_threshold = CONFIG["feature_selection"]["correlation_threshold"]
        preprocessing_pipelines = ml.build_preprocessing_pipeline(
            feature_selection,
            remove_lowvariance_features,
            remove_highcorrelation_features,
            variance_threshold,
            correlation_threshold,
            random_state,
        )

        for preprocessing_pipeline in preprocessing_pipelines:
            ml.init_preprocessing_pipeline(preprocessing_pipeline)

            (
                feature_names,
                X_train_os,
                X_train,
                X_test,
                X_mbval_structure,
                X_mbval_sirius,
            ) = ml.preprocess_all_sets(
                preprocessing_pipeline,
                feature_names,
                X_train_os,
                y_train_os,
                X_train,
                X_test,
                X_mbval_structure,
                X_mbval_sirius,
            )

            # Get the label counts
            ml.log_binarized_label_count(y, "TOTAL", activity_threshold)
            ml.log_binarized_label_count(y_train_os, "TRAIN", activity_threshold)
            ml.log_binarized_label_count(y_test, "TEST", activity_threshold)
            ml.log_binarized_label_count(
                y_mbval, "MassBank VALIDATION", activity_threshold
            )

            LOGGER.info("Run pipeline for all estimators:\n")
            # Build for each estimator a pipeline according to the configurations in the config file
            for estimator in CONFIG_ESTIMATORS["estimators"]:
                start_time = datetime.now()

                # Init a new folder for this estimator
                estimator_name = estimator["name"]
                ESTIMATOR_PIPELINE = ml.init_estimator_pipeline(estimator_name)
                LOGGER.info(f"Apply {ESTIMATOR_PIPELINE}")

                ## Training
                # Build the pipeline for the current estimator with the specified parameter grid
                pipeline = ml.build_pipeline(estimator, random_state)

                # Perform grid search cross-validation
                # (Note: CV on TRAINING set with RepeatedStratifiedKFold)
                LOGGER.info("Start Grid Search Cross-Validation..")
                n_splits = CONFIG["grid_search_cv"]["n_splits"]
                n_repeats = CONFIG["grid_search_cv"]["n_repeats"]
                grid_search = ml.perform_grid_search_cv(
                    X_train_os,
                    y_train_os,
                    estimator,
                    pipeline,
                    n_splits,
                    n_repeats,
                    random_state,
                )
                LOGGER.info("Training Done.\n")

                # Save best estimator (estimator with best performing parameters from grid search)
                best_estimator = grid_search.best_estimator_
                ml.save_model(best_estimator, "train")

                ## Validation
                # Predict on the test set with the best estimator (X_test, y_test is unseen)
                LOGGER.info("Start Internal Testing")
                validation_set = ml.init_validation_set("test")
                LOGGER.info("+" * 60)
                LOGGER.info(f"Predict ({validation_set})")
                default_threshold = CONFIG["threshold_moving"]["default_threshold"]
                threshold_moving = CONFIG["apply"]["threshold_moving"]
                target_tpr = CONFIG["threshold_moving"]["target_tpr"]
                target_tnr = CONFIG["threshold_moving"]["target_tnr"]
                cost_tpr = CONFIG["threshold_moving"]["cost_tpr"]
                cost_fpr = CONFIG["threshold_moving"]["cost_fpr"]
                ml.predict_and_report_classification(
                    X_test,
                    y_test,
                    best_estimator,
                    default_threshold,
                    threshold_moving,
                    target_tpr,
                    target_tnr,
                    cost_tpr,
                    cost_fpr,
                )
                LOGGER.info("Internal Testing Done.\n")

                # Retrain the best estimator from GridSearchCV with train and test data
                ml.init_estimator_pipeline(estimator_name)
                LOGGER.info("Retrain on train/test set..\n")
                X_combined = np.vstack((X_train, X_test))
                y_combined = np.concatenate((y_train, y_test))
                if oversampling == 1:
                    LOGGER.info(" oversampling of train/test dataset is running")
                    LOGGER.info("#" * 60)
                    X_combined_os, y_combined_os = ml.handle_oversampling(
                        X_combined,
                        y_combined,
                        random_state,
                    )
                else:
                    X_combined_os = X_combined.copy()
                    y_combined_os = y_combined.copy()
                best_estimator.fit(
                    X_combined_os,
                    y_combined_os,
                )
                ml.save_model(best_estimator, "train_test")

                # Predict on the 1. "true Massbank" and 2. "SIRIUS predicted" validation set
                LOGGER.info("Start MassBank Validation")
                validation_set_names = ["structure", "sirius"]
                validation_sets = [
                    X_mbval_structure,
                    X_mbval_sirius,
                ]
                for name, X_mbval in zip(validation_set_names, validation_sets):
                    validation_set = ml.init_validation_set(f"mb_val_{name}")
                    LOGGER.info("+" * 60)
                    LOGGER.info(f"Predict ({validation_set})")
                    ml.predict_and_report_classification(
                        X_mbval,
                        y_mbval,
                        best_estimator,
                        default_threshold,
                        threshold_moving,
                        target_tpr,
                        target_tnr,
                        cost_tpr,
                        cost_fpr,
                    )

                LOGGER.info("MassBank Validation Done.\n")

                # Retrain the estimator on full data for future predictions
                ml.init_estimator_pipeline(estimator_name)
                LOGGER.info("Retrain on full data..\n")
                X_all = np.vstack((X_combined, X_mbval_structure))
                y_all = np.concatenate((y_combined, y_mbval))
                if oversampling == 1:
                    LOGGER.info(" oversampling of full dataset is running")
                    LOGGER.info("#" * 60)
                    X_all_os, y_all_os = ml.handle_oversampling(
                        X_all,
                        y_all,
                        random_state,
                    )
                else:
                    X_all_os = X_all.copy()
                    y_all_os = y_all.copy()
                best_estimator.fit(X_all_os, y_all_os)
                ml.save_model(best_estimator, "full_data")

                # Get feature importances
                # (only implemented for XGB and RandomForest)
                ml.get_feature_importance_if_applicable(best_estimator, feature_names)

                # Time elapsed
                elapsed = round((datetime.now() - start_time).total_seconds(), 2)
                LOGGER.info(f"Done {estimator['name']} >> {elapsed} seconds.\n\n\n")

    except Exception as e:
        traceback_info = traceback.format_exc()
        ml.report_exception(e, traceback_info, aeid)

        # Write a failed flag file to the aeid folder
        ml.init_aeid(aeid)  # re-init aeid's DUMP_FOLDER
        ml.add_status_file("failed")

# Calculate the total elapsed time
LOGGER.info(f"Finished all: Total time >> { ml.get_total_elapsed_time()}\n")

# store aeid file
aeid_df = pd.DataFrame(selected_aeid_list, columns=["aeid"]).astype("int")
aeid_df = pd.merge(aeid_df, aeid_info_df, on="aeid", how="left")
selected_aeid_file = Path(LOG_PATH) / SELECTED_AEIDS
aeid_df.sort_values("aeid").round(5).to_csv(selected_aeid_file, index=False)
print(f"Processed and saved to file: {selected_aeid_file}")

# copy true training fps file to run folder
shutil.copy2(fps_input_file, LOG_PATH)
print(f"Copied true training fps file to {LOG_PATH}")
