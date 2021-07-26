#!/bin/bash

src=$(pwd)
faceroot=~/maw_face_recognition
facedb="${faceroot}/faces"
facetests="${faceroot}/faces_test"
unknown_faces="${faceroot}/faces_unknown"

podman run \
    -it \
    --rm \
    -v "${src}/src":/src \
    -v "${src}/test":/test \
    -v "${facedb}":/facedb \
    -v "${facetests}":/facetests \
    -v "${unknown_faces}":/faces_unkown \
    --hooks-dir=/usr/share/containers/oci/hooks.d/ \
    --security-opt label=disable \
    maw-facerec
