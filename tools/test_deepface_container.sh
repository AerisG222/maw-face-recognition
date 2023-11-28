#!/bin/bash

# :: ways to test the custom container ::

# 1. confirm tensorflow will use gpu:
# python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

# 2. run test of our script
# python /mnt/scripts/main.py /mnt/facedb /mnt/images /mnt/results/out1.csv

podman run \
    -it \
    --rm \
    --device nvidia.com/gpu=all \
    --security-opt=label=disable \
    --volume ~/git/maw-face-recognition/src:/mnt/scripts \
    --volume ~/maw_face_recognition/face_db:/mnt/facedb \
    --volume ~/maw_face_recognition/test_images:/mnt/images \
    --volume ~/maw_face_recognition/results:/mnt/results \
    localhost/maw-facerec:latest \
    python /mnt/scripts/main.py /mnt/facedb /mnt/images /mnt/results/out1.csv y | grep '*'
