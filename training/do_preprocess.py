from algorithm.preprocess import preprocess
import os
import glob
import SimpleITK as sitk
import numpy as np
import shutil
import paths


def main(in_dir, out_dir):
    # iterate over all files in the training set
    output_image_dir = os.path.join(out_dir, "data/npy/")
    os.makedirs(output_image_dir, exist_ok=True)

    for filename in glob.glob(os.path.join(in_dir, "data/mha/*")):
        # load each file with SimpleITK
        sitk_image = sitk.ReadImage(filename)

        # preprocess each file
        image = preprocess(sitk_image)

        # save each file as npy
        out_filename = os.path.basename(os.path.splitext(filename)[0] + ".npy")
        np.save(os.path.join(output_image_dir, out_filename), image)
        print(f"Image {filename} processed.")

    # Copy metadata
    if out_dir != in_dir:
        output_metadata_dir = os.path.join(out_dir, "metadata")
        os.makedirs(output_metadata_dir, exist_ok=True)
        shutil.copyfile(os.path.join(in_dir, 'metadata/reference.csv'),
                        os.path.join(out_dir, 'metadata/reference.csv'))


if __name__ == "__main__":
    main(in_dir=paths.PREPROCESS_INPUT_DIR, out_dir=paths.PREPROCESS_OUTPUT_DIR)
