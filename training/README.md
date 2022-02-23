# STOIC2021 Final Phase Training Example 

This folder contains an example for generating a Docker container that can train a model on [the public training data](https://registry.opendata.aws/stoic2021-training/) of the STOIC2021 challenge.

## Table of Contents
* [Building, testing and exporting your training container](#buildtestexport)
* [Implementing your own training algorithm](#implementing)

<a id="buildtestexport"></a>
## Building, testing, and exporting your training container 
### Building
To test if your system is set up correctly, you can run `./build.sh` (Linux) or `./build.bat` (Windows), that simply implement this command:

```docker build -t stoictrain .```

Please note that the next step (testing the container) also runs a build, so this step is not necessary if you are certain that everything is set up correctly.

<a name="testing"></a>
### Testing
To test if the docker container works as expected, make sure that the [STOIC2021 public training set](https://registry.opendata.aws/stoic2021-training/) has been downloaded to `/path/to/stoic2021-training/`. 

**Note: Running the following command will delete the current contents of `../inference/artifact/`.**

You can now run:

```bash test.sh /path/to/stoic2021-training/```

if you are on Linux, or:

```test.bat \path\to\stoic2021-training\```

if you are on Windows.

`test.sh`/`test.bat` will build the container and train your algorithm with the public training set. It will produce trained model weights in the `../inference/artifact/` directory to be used later for generating the inference Docker container. 

If the test runs successfully, you will see you will see `Training completed.`, and your model weights will have been saved to `../inference/artifact/`.

Note: If you do not have a GPU available on your system, remove the `--gpus all` flag in `test.sh`/`test.bat` to run the test. 


<a name="exporting"></a>
### Exporting
Run `export.sh`/`export.bat` to save the Docker image to `./STOICTrain.tar.gz`. This script runs `build.sh`/`build.bat` as well as the following command:
`docker save stoictrain | gzip -c > STOICTrain.tar.gz`

Please note that it is not necessary to include the resulting `STOICTrain.tar.gz` file in your submission. The challenge organizers will build and save a new Docker image using your submission. This new Docker image will be used to train your algorithm on the full (public + private) training set.

<a id="implementing"></a>
## Implementing your own training algorithm
You can implement your own solution by altering the [`do_learning`](https://github.com/luukboulogne/stoic2021-baseline-finalphase/blob/a9916c6a2a8c075300200e0d0c04dfffe93b0b17/training/train.py#L76) function in `./train.py`. See the documentation of this function in `./train.py` for more information.

Any additional imported packages needed for inference should be added to `./requirements.txt`, and any additional files and folders you add should be explicitly copied in the `./Dockerfile`. See `./requirements.txt` and `./Dockerfile` for examples. After implementing your own algorithm, make sure that your training codebase is ready for submission by [testing](#testing) it.

Please note that your container will not have access to the internet when executing on grand-challenge.org, so any pre-trained model weights must be present in your container image. You can test this locally using the `--network=none` option of `docker run`.

After implementing your own training Docker container, you can implement your inference container. For this, please refer to [`../inference/README.md`](https://github.com/luukboulogne/stoic2021-baseline-finalphase/tree/master/inference).

