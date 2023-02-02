from algorithm.preprocess import preprocess
from pathlib import Path
import SimpleITK as sitk
import numpy as np
import shutil
import paths
import logging
import multiprocessing

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s][%(asctime)s] %(message)s",
    datefmt="%I:%M:%S",
)


def preprocess_and_save_one_image(
    input_fname: Path,
    output_fname: Path,
) -> None:
    """Function to preprocess one mha file and save as numpy file

    Args:
        input_fname (Path): Path to input .mha file
        output_fname (Path): Path to output .npy file
    """

    # load each file with SimpleITK
    sitk_image = sitk.ReadImage(str(input_fname))

    # preprocess each file
    image = preprocess(sitk_image)

    # save each file as npy
    np.save(output_fname, image)
    logging.info(f"Image {input_fname} processed.")


def main(
    in_dir: Path,
    out_dir: Path,
    num_workers: int = 1,
) -> None:
    """Function to preprocess all images for the STOIC training set
    All mha files (3D volumes) are first loaded through SimpleITK, preprocessed, and then saved as numpy files

    Args:
        in_dir (Path): Path to raw data from the STOIC dataset
        out_dir (Path): Path to save the preprocessed numpy files
        num_workers (int, optional): Number of parallel works to initiate. Defaults to 1.
    """

    # create output directories for storing numpy files
    output_image_dir = out_dir / "data" / "npy"
    output_image_dir.mkdir(exist_ok=True, parents=True)

    # compile input (.mha) and output (.npy) file pairs
    input_output_pairs = [
        [input_fname, output_image_dir / f"{input_fname.stem}.npy"]
        for input_fname in (in_dir / "data" / "mha").glob("*.mha")
    ]

    # preprocess all images with multi-threading
    pool = multiprocessing.Pool(num_workers)
    pool.starmap(preprocess_and_save_one_image, input_output_pairs)
    pool.close()

    # Copy metadata
    if out_dir != in_dir:

        output_metadata_dir = out_dir / "metadata"
        output_metadata_dir.mkdir(exist_ok=True, parents=True)

        shutil.copyfile(
            in_dir / "metadata" / "reference.csv",
            out_dir / "metadata" / "reference.csv",
        )


if __name__ == "__main__":
    main(
        in_dir=paths.PREPROCESS_INPUT_DIR_SAGEMAKER, 
        out_dir=paths.PREPROCESS_OUTPUT_DIR_SAGEMAKER,
        num_workers=16,
    )
