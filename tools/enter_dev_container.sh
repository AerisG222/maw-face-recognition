#!/bin/bash

src=$(pwd)
faceroot=~/maw_face_recognition
facedb="${faceroot}/face_db"
test_image_root="${faceroot}/test_images"
real_image_root="/srv/www/website_assets/images"
found_faces="${faceroot}/faces_found"
unknown_faces="${faceroot}/faces_unknown"

podman run \
    -it \
    --rm \
    -v "${src}/src":/src \
    -v "${src}/test":/test \
    -v "${facedb}":/face_db \
    -v "${test_image_root}":/test_images \
    -v "${real_image_root}":/real_images \
    -v "${found_faces}":/faces_found \
    -v "${unknown_faces}":/faces_unknown \
    --hooks-dir=/usr/share/containers/oci/hooks.d/ \
    --security-opt label=disable \
    maw-facerec
