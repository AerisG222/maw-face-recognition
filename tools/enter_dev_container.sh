#!/bin/bash

src=$(pwd)
faceroot=~/maw_face_recognition
test_image_root="${faceroot}/test_images"
real_image_root="/srv/www/website_assets/images"
dfroot="${faceroot}/deepface"
frroot="${faceroot}/face_recognition"

podman run \
    -it \
    --rm \
    -v "${src}/src":/src \
    -v "${src}/test":/test \
    -v "${test_image_root}":/test_images \
    -v "${real_image_root}":/real_images \
    -v "${dfroot}":/deepface \
    -v "${frroot}":/facerecognition \
    --hooks-dir=/usr/share/containers/oci/hooks.d/ \
    --security-opt label=disable \
    maw-facerec
