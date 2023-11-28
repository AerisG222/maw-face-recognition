#!/bin/bash
SCRIPT_DIR=~/git/maw-face-recognition/src
FACEDB_DIR=~/maw_face_recognition/face_db
RESULT_DIR=~/maw_face_recognition/results
IMGROOT=/srv/www/website_assets/images
EXTRACT_FACES=y

ESCAPE_PATH_FOR_REGEX='s/\//\\\//g'
IMGDIRS=$(find $IMGROOT -type d -name md)
IMGROOT_REGEX=$(echo "^${IMGROOT}/" | sed -e "${ESCAPE_PATH_FOR_REGEX}")

build_mountdir() {
    local DIR=$1

    # this will result in a path like /images/2023/ab_vs_lincoln/md
    # which perfectly matches how this will be stored in the photo database for easy
    # matching during the loading process (not yet built)
    echo "${DIR}" | \
        sed -e "s/${IMGROOT_REGEX}/\/images\//"
}

build_outfile() {
    local DIR=$1

    # get start and end paths with separater escaped so it can be used in later calls to sed
    local END_PATH_TO_REMOVE="$(echo "/md\$" | sed -e "${ESCAPE_PATH_FOR_REGEX}")"

    echo "${DIR}" | \
        sed -e "s/${IMGROOT_REGEX}//" | \
        sed -e "s/${END_PATH_TO_REMOVE}/\.csv/" | \
        sed -e "s/\//__/g"
}

facerec() {
    local DIR=$1
    local MOUNT_DIR=$(build_mountdir "${DIR}")
    local OUTFILE=$(build_outfile "${DIR}")

    if [ -f "${RESULT_DIR}/${OUTFILE}" ]; then
        return
    fi

    podman run \
        -it \
        --rm \
        --device nvidia.com/gpu=all \
        --security-opt=label=disable \
        --volume "${SCRIPT_DIR}":/mnt/scripts \
        --volume "${FACEDB_DIR}":/mnt/facedb \
        --volume "${DIR}":"${MOUNT_DIR}" \
        --volume "${RESULT_DIR}":/mnt/results \
        localhost/maw-facerec:latest \
        python /mnt/scripts/main.py /mnt/facedb "${MOUNT_DIR}" /mnt/results/${OUTFILE} ${EXTRACT_FACES} | grep '*'
}

for DIR in ${IMGDIRS[@]}; do
    facerec $DIR
done
