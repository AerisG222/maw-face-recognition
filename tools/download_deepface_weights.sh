#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
MODEL_DIR="${SCRIPT_DIR}/faces_model_weights"
SERENGIL_MODEL_BASE_URL="https://github.com/serengil/deepface_models/releases/download/v1.0"
SERENGIL_MODELS=(
    "age_model_weights.h5"
    "arcface_weights.h5"
    "deepid_keras_weights.h5"
    "facenet512_weights.h5"
    "facenet_weights.h5"
    "facial_expression_model_weights.h5"
    "gender_model_weights.h5"
    "openface_weights.h5"
    "race_model_single_batch.h5"
    "retinaface.h5"
    "vgg_face_weights.h5"
)

if [ ! -d "${MODEL_DIR}" ]; then
    mkdir "${MODEL_DIR}"
fi

pushd "${MODEL_DIR}"

for MODEL in ${SERENGIL_MODELS[@]}
do
    if [ ! -f "${MODEL}" ]; then
        curl -JLO "${SERENGIL_MODEL_BASE_URL}/${MODEL}"
    fi
done

# this ends up getting referenced by the vggface2 model, so pull this down ahead of time
curl -JLO "https://github.com/swghosh/DeepFace/releases/download/weights-vggface2-2d-aligned/VGGFace2_DeepFace_weights_val-0.9034.h5.zip"
unzip VGGFace2_DeepFace_weights_val-0.9034.h5.zip
rm VGGFace2_DeepFace_weights_val-0.9034.h5.zip

popd
