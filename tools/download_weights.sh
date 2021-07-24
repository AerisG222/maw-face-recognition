#!/bin/bash

modeldir=~/faces_model_weights

models=(
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

pushd "${modeldir}"

for model in ${models[@]}
do
    if [ ! -f "${model}" ]; then
        curl -JLO "https://github.com/serengil/deepface_models/releases/download/v1.0/${model}"
    fi
done

popd
