#!/bin/bash

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
    python /mnt/scripts/main.py /mnt/facedb /mnt/images /mnt/results/out1.csv
