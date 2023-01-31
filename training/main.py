import shutil
from train import do_learning
import paths

if __name__ == "__main__":
    # Substitute do_learning for your training function.
    # It is recommended to write artifacts (e.g. model weights) to ARTIFACT_DIR during training.
    artifacts = do_learning(paths.TRAINING_INPUT_DIR, paths.TRAINING_OUTPUT_DIR)

    # When the learning has completed, any artifacts should have been saved to ARTIFACT_DIR.
    # Alternatively, you can copy artifacts to ARTIFACT_DIR after the learning has completed:
    for artifact in artifacts:
        shutil.copy(artifact, paths.TRAINING_OUTPUT_DIR)

    print("Training completed.")
