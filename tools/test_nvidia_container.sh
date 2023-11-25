podman run \
    -it \
    --rm \
    --device nvidia.com/gpu=all \
    --security-opt=label=disable \
    nvcr.io/nvidia/tensorflow:23.10-tf2-py3 \
    nvidia-smi -L
