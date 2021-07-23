#!/bin/bash

src=$(pwd)

podman run \
    -it \
    --rm \
    -v "${src}/src":/src \
    --hooks-dir=/usr/share/containers/oci/hooks.d/ \
    --security-opt label=disable \
    nvcr.io/nvidia/tensorflow:21.06-tf2-py3
