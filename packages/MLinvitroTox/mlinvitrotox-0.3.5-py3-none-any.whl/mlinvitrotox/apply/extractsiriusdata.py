import glob
import zipfile

from pathlib import Path

import filetype
from tqdm import tqdm
import click


def extract_and_find_zips(zip_path, output_dir=None):
    # Convert paths to Path objects
    zip_path = Path(zip_path)

    if not zip_path.is_file() and output_dir is not None:
        raise RuntimeError("If SIRIUS input is a folder, output dir must be omitted")

    if output_dir is None:
        output_dir = zip_path.with_suffix("")

    output_dir = Path(output_dir)
    # Ensure the output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Extract the main zip file
    if zip_path.is_file():
        print(f"Unzipping {zip_path}")
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(output_dir)

    # Recursively find and extract other zip files using glob
    def extract_nested_zips(directory):
        # Use glob to recursively find all files in the directory
        file_paths = glob.glob(f"{directory}/**/*", recursive=True)
        for file_path in tqdm(file_paths, desc="Processing files"):
            file = Path(file_path)
            if file.is_file():
                # Check if the file is a zip file
                kind = filetype.guess(file)
                if kind and kind.extension == "zip":
                    # Extract nested zip file
                    with zipfile.ZipFile(file, "r") as nested_zip_ref:
                        nested_zip_ref.extractall(file.parent)

    # Start the recursive search and extraction process
    extract_nested_zips(output_dir)

    print(f"Extracted the SIRIUS data {zip_path} to {output_dir}/")


@click.command("extract")
@click.option(
    "--sirius_input",
    "-i",
    help="path to SIRIUS ZIP file or folder of SIRIUS content",
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--output_folder",
    "-o",
    default=None,
    help="path to directory where the processed output should be stored. It will be created if it does not exist.",
)
def extract_sirius_data(sirius_input, output_folder):
    """
    Extract data from SIRIUS

    """
    extract_and_find_zips(sirius_input, output_folder)


if __name__ == "__main__":
    extract_sirius_data()
