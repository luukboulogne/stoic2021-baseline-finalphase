#!/usr/bin/env bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

./build.sh

# make the artifact folder writable
chmod 777 $SCRIPTPATH/../inference/artifact/

# Clear the artifact folder
rm -r $SCRIPTPATH/../inference/artifact/*

# Run the algorithm
MEMORY="108g"

docker run --rm --gpus all \
        --memory=$MEMORY --memory-swap=$MEMORY \
        --cap-drop=ALL --security-opt="no-new-privileges" \
        --network none --shm-size=20g --pids-limit 256 \
        -v $1:/input/ \
        -v $SCRIPTPATH/../inference/artifact/:/output/ \
        stoictrain
