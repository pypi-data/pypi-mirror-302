import joblib
import zipfile
import shutil
import requests
import toml
from io import StringIO

from pathlib import Path

import pandas as pd

import click
from tqdm import tqdm

import mlinvitrotox.utils.training as ml
import mlinvitrotox.utils.get_predicted_fps as get_predfps
import mlinvitrotox.utils.predict as predict

SELECTED_AEIDS = "selected_aeids.csv"
SELECTED_CHEMICALS = "selected_chemicals.csv"


class Model:
    model_repo = "https://zenodo.org/records/13323297/files/"

    def __init__(
        self, target_variable: str = "hitcall_c", ml_algorithm: str = "classification"
    ) -> None:
        self.target_variable = target_variable
        self.ml_algorithm = ml_algorithm

    def load(self, path: str | Path):
        model_path = Path(path)
        self.model_path = model_path

        # if it doesn't exist, check if it's a model name that we can download from zenodo
        if not model_path.exists():
            try:
                model_name = model_path.with_suffix("")
                model_path = self.download(model_name)
            except RuntimeError as e:
                raise FileNotFoundError(
                    f"Could not find the model file {model_path}. To use the provided models, specify '-m mlinvitrotox_model'."
                )

        if model_path.suffix == ".itox":
            # Open the zip file
            zip_ref = zipfile.ZipFile(model_path, "r")

            def get_path(sub_path):
                # Open the specific CSV file inside the zip
                try:
                    return zip_ref.open(Path(sub_path).as_posix())
                except KeyError as e:
                    raise FileNotFoundError(e)
        elif model_path.is_dir():

            def get_path(sub_path):
                return model_path / sub_path
        else:
            raise RuntimeError(f"Failed to open file {model_path}")

        self.get_path = get_path

        # load true training fingerprints
        training_fps_path = get_path("training_true-fps.parquet")
        self.df_truefps = ml.get_fingerprint_df(training_fps_path)

        # load logged assay information overview
        assay_info_path = get_path(SELECTED_AEIDS)
        df_assay_info = pd.read_csv(assay_info_path)
        df_assay_info["aeid"] = df_assay_info["aeid"].astype("str")
        self.df_assay_info = df_assay_info

        # load metrics file
        metrics_path = get_path("modeltraining_metrics.csv")
        df_metrics = pd.read_csv(metrics_path)
        df_metrics["aeid"] = df_metrics["aeid"].astype("int")
        self.df_metrics = df_metrics.sort_values("aeid")

    def download(self, model_name: str):
        url = self.model_repo + "/" + str(model_name) + ".itox"
        appdir = Path(click.get_app_dir("mlinvitrotox"))

        appdir.mkdir(parents=True, exist_ok=True)

        # Define the path to the TOML file
        toml_file = Path(appdir) / "config.toml"

        # Default value for "model_cache"
        default_value = Path(appdir) / "model_cache/"

        default_value.mkdir(parents=True, exist_ok=True)

        # Check if the file exists
        if toml_file.exists():
            # Load the existing TOML file
            with open(toml_file, "r") as file:
                config = toml.load(file)
                model_cache = config.get("model_cache", str(default_value))
        else:
            # File does not exist, create it with default values
            config = {"model_cache": str(default_value)}
            with open(toml_file, "w") as file:
                toml.dump(config, file)
            model_cache = Path(default_value)

        local_filename = Path(model_cache) / f"{model_name}.itox"

        if local_filename.exists():
            return local_filename

        # Send a GET request to the URL
        response = requests.get(url, stream=True)

        if not response.ok:
            raise RuntimeError(
                f"Could not find the model {model_name} in the online model repository."
            )

        print("Downloading file ")
        # Open the local file in write-binary mode and save the contents
        with open(local_filename, "wb") as file:
            for chunk in tqdm(response.iter_content(chunk_size=8192)):
                file.write(chunk)

        print(f"Downloaded {local_filename} from {url}")

        return local_filename

    def predict(self, df_predfps):
        # only keep fingerprints bits used for training
        df_predfps_selected = get_predfps.keep_selected_fps_bits(
            df_predfps,
            self.df_truefps,
        )

        # initialize
        list_dfs_pred = []

        # for each aeid
        aeids = self.df_assay_info["aeid"].astype("str").to_list()

        for aeid in tqdm(aeids, desc="Processing AEIDs"):
            df_pred = self.predict_aeid(aeid, df_predfps_selected)
            if df_pred is not None:
                list_dfs_pred.append(df_pred)

        # concatenate
        df_predictions = pd.concat(list_dfs_pred)
        df_predictions["prediction"] = df_predictions["prediction"].astype(int)

        # merge predictions with assay information
        df_predictions = pd.merge(
            df_predictions,
            self.df_assay_info[["aeid", "MechanisticTarget", "signal_direction"]],
            on="aeid",
            how="left",
        )

        # Calculate score per endpoint
        df_predictions = predict.calculate_endpoint_score(df_predictions)

        return df_predictions

    def predict_aeid(self, aeid, df_predfps_selected):
        chem_ids = df_predfps_selected.index

        aeid_path = Path(self.target_variable) / self.ml_algorithm / str(aeid)
        if True:  # TODO add a check if file exists
            # get true fingerprints for selected chemicals
            selected_chemicals_file = self.get_path(aeid_path / SELECTED_CHEMICALS)
            df_truefps_selected = predict.get_true_fingerprints_for_selected_chemicals(
                selected_chemicals_file,
                self.df_truefps,
                self.target_variable,
            )

            # load classifier and preprocessing pipeline
            preproc_path = aeid_path / "Feature_Selection_RandomForestClassifier"
            try:
                preprocessor_path = self.get_path(
                    Path(preproc_path) / "preprocessing_model.joblib"
                )
                preprocessor = joblib.load(preprocessor_path)
            except FileNotFoundError:
                preprocessor = None

            try:
                classifier_path = self.get_path(
                    Path(preproc_path)
                    / "XGBClassifier"
                    / "best_estimator_full_data.joblib"
                )
                classifier = joblib.load(classifier_path)
            except FileNotFoundError:
                classifier = None

            # catch unsuccessful runs
            if classifier is None:
                return None
            # preprocess fingerprints
            preprocessed_truefps = preprocessor.transform(df_truefps_selected)
            preprocessed_predfps = preprocessor.transform(df_predfps_selected)

            # calculate maximum cosine similarity
            max_similarities = predict.calculate_maximum_similarity(
                preprocessed_predfps,
                preprocessed_truefps,
            )

            # calculate predictions for each data point
            df_pred = predict.calculate_predictions(
                classifier,
                preprocessed_predfps,
                chem_ids,
                max_similarities,
                aeid,
            )
            return df_pred

    def export(self, filepath: str | Path, export_stats=False):
        """Exports current model to an .itox file at the given path

        Args:
            filepath (str | Path): the path to the .itox file to be created
            export_stats (boolean): if the statistics files should be exported as well

        """
        filepath = Path(filepath)
        if filepath.suffix != ".itox" and not filepath.is_dir():
            raise RuntimeError(
                f"Wrong file type of target. Export targets can only be .itox file or an existing directory.\nProvided filepath is {filepath}"
            )

        if self.model_path.suffix == ".itox":
            # since we already have an (immutable) itox file we can just copy it
            shutil.copy(
                self.model_path,
                filepath,
            )
        elif self.model_path.is_dir():
            # We need to collect all relevant files for export
            if filepath.is_dir():
                # make the output have the same filename as the original
                filepath = filepath / self.model_path.with_suffix(".itox").name

            include_list = []

            # add base
            include_list += [self.model_path / "modeltraining_metrics.csv"]
            include_list += [self.model_path / "training_true-fps.parquet"]
            # selected_aeids.csv will be created later

            # add logs
            include_list += [self.model_path / "log" / "modelfitting.log"]

            # for each aeid
            failed_aeids = []
            aeid_folders = self.model_path / self.target_variable / self.ml_algorithm
            for aeid_folder in aeid_folders.glob("*/"):
                if (
                    aeid_folder / "Feature_Selection_RandomForestClassifier"
                    not in aeid_folder.iterdir()
                ):
                    continue
                if aeid_folder / "failed.txt" in aeid_folder.iterdir():
                    failed_aeids += [int(aeid_folder.stem)]
                    continue

                include_list += [aeid_folder / "selected_chemicals.csv"]
                feature_selection_path = (
                    aeid_folder / "Feature_Selection_RandomForestClassifier"
                )
                include_list += [feature_selection_path / "preprocessing_model.joblib"]
                include_list += [feature_selection_path / "selected_features.csv"]
                estimator_path = (
                    aeid_folder
                    / "Feature_Selection_RandomForestClassifier"
                    / "XGBClassifier"
                )
                include_list += [estimator_path / "best_estimator_full_data.joblib"]

                # add metric folders
                if export_stats:
                    include_list += list(estimator_path.rglob("mb_val_sirius/*"))
                    include_list += list(estimator_path.rglob("mb_val_structure/*"))
                    include_list += list(estimator_path.rglob("test/*"))

            # update selected aeids files to not contain failed aeids
            selected_aeids_path = self.get_path("selected_aeids.csv")
            df = pd.read_csv(selected_aeids_path)
            df = df[~df["aeid"].isin(failed_aeids)]

            # Writing the files to the zipfile
            with zipfile.ZipFile(
                filepath, "w", compression=zipfile.ZIP_DEFLATED
            ) as zipf:
                for path in tqdm(include_list):
                    zipf.write(path, arcname=path.relative_to(self.model_path))

                # write the selected_aeids.csv
                csv_buffer = StringIO()
                df.to_csv(csv_buffer, index=False)
                zipf.writestr("selected_aeids.csv", csv_buffer.getvalue())
        else:
            raise RuntimeError(f"Unkown model file {self.model_path}")

    def copy_metrics(self):
        pass