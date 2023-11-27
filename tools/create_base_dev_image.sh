#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
MODEL_DIR="${SCRIPT_DIR}/faces_model_weights"

if [ ! -d "${MODEL_DIR}" ]; then
    echo "Please run download_deepface_weights.sh first!"
    exit
fi

buildah bud -f "${SCRIPT_DIR}/Containerfile" -t maw-facerec "${SCRIPT_DIR}"
