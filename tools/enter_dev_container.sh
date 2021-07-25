#!/bin/bash

src=$(pwd)
facedb=~/faces
facetests=~/faces_test

podman run \
    -it \
    --rm \
    -v "${src}/src":/src \
    -v "${src}/test":/test \
    -v "${facedb}":/facedb \
    -v "${facetests}":/facetests \
    --hooks-dir=/usr/share/containers/oci/hooks.d/ \
    --security-opt label=disable \
    maw-facerec
