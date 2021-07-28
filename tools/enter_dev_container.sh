#!/bin/bash

src=$(pwd)
faceroot=~/maw_face_recognition
facedb="${faceroot}/face_db"
facetests="${faceroot}/face_tests"
found_faces="${faceroot}/faces_found"
unknown_faces="${faceroot}/faces_unknown"

podman run \
    -it \
    --rm \
    -v "${src}/src":/src \
    -v "${src}/test":/test \
    -v "${facedb}":/face_db \
    -v "${facetests}":/face_tests \
    -v "${found_faces}":/faces_found \
    -v "${unknown_faces}":/faces_unknown \
    --hooks-dir=/usr/share/containers/oci/hooks.d/ \
    --security-opt label=disable \
    maw-facerec
