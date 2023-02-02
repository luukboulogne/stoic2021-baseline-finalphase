import os
from pathlib import Path

def get_path_from_env(path):
    path = os.getenv(path)
    if path is None:
        return None
    else:
        return Path(path)

PREPROCESS_INPUT_DIR = Path("/input/")
PREPROCESS_OUTPUT_DIR = Path("/scratch/")

TRAINING_INPUT_DIR = Path("/scratch/")
TRAINING_OUTPUT_DIR = Path("/output/")


PREPROCESS_INPUT_DIR_SAGEMAKER = get_path_from_env('SM_CHANNEL_DATASET')
PREPROCESS_OUTPUT_DIR_SAGEMAKER = Path('/preprocessed/')

TRAINING_INPUT_DIR_SAGEMAKER = get_path_from_env('SM_CHANNEL_PREPROCESSED')
TRAINING_OUTPUT_DIR_SAGEMAKER = Path("/artifact/")
