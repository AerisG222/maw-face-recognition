# Face Recognition tool for mikeandwan.us photos

## Prep

1. Make sure podman + nvidia drivers are installed
2. Follow post: https://www.quora.com/How-can-TensorFlow-with-NVIDIA-GPU-support-be-installed-on-Fedora-32
3. `tools/test_nvidia_container.sh`
4. Edit /etc/nvidia-container-runtime/config.toml to specify no-cgroups=true
5. step 3 should now indicate permission error
6. `sudo chcon -t container_file_t /dev/nvidia*` to relax selinux
7. step 3 now works!

### Prepare Custom Image

This will prepare an image based off the nvidia image containing the tools we will use.
Currently, there is an issue when running the `buildah` command below as a rootless user.
This error said something about an invalid device link, and after some googling, came across
the following workaround:

Go to the following page, then scroll to the bottom for the item labeled:
[Rootless buildah bud fails when using OverlayFS](https://github.com/containers/buildah/blob/main/troubleshooting.md#6-rootless-buildah-bud-fails-when-using-overlayfs)

To fix, create the file `~/.config/containers/storage.conf` and add the following to it:

```ini
[storage]
# Default Storage Driver, Must be set for proper operation.
driver = "overlay"

[storage.options]
# Storage options to be passed to underlying storage drivers
mount_program = "/usr/bin/fuse-overlayfs"
```

After that, run `tools/create_base_dev_image.sh` and the buildah command worked.  Once that is done,
you will have a local image named `maw-facerec` that can be used.

## Dev

Run the dev container, with source from this project mounted in /src:

```bash
tools/enter_dev_container.sh
```

## Approach

The goal of this project is to provide a framework for evaluating faces in photos for mikeandwan.us.
In this regard, it is expected that the user will go through the process of extracting individual
faces and placing them in directories named after the person.  Right now, it is expected that only a few
representative images are needed per person, but that will need to be evaluated further.  Once
that directory of classified images is in place, you should then be able to run the program
against the full catalog of images, and have it spit out found and/or recognized face information.
This can then be stored in a database so that it can be available as additional metadata for the photos
and eventually incorporated into the photos application.

## References

- https://github.com/serengil/deepface
- https://github.com/ageitgey/face_recognition
- https://www.mdpi.com/1999-5903/13/7/164
- https://machinelearningmastery.com/how-to-perform-face-recognition-with-vggface2-convolutional-neural-network-in-keras/
- https://keras.io/guides/transfer_learning/
- https://medium.com/analytics-vidhya/face-recognition-with-vgg-face-in-keras-96e6bc1951d5


## Setup steps to run via podman container (Fedora 39)

the following steps can be used via cpu for quick testing:

```
sudo dnf install python3.11
python3.11 -m pip install tensorflow[and-cuda]
python3.11 -m pip install deepface
```

the following is to fully configure the nvidia container environment (assumes nvidia drivers already installed):
https://catalog.ngc.nvidia.com/orgs/nvidia/containers/tensorflow
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html#installing-with-yum-or-dnf
https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/cdi-support.html

1. install container toolkit
```
curl -s -L https://nvidia.github.io/libnvidia-container/stable/rpm/nvidia-container-toolkit.repo |   sudo tee /etc/yum.repos.d/nvidia-container-toolkit.repo

sudo yum install -y nvidia-container-toolkit
```

2. configure container device interface (CDI)

```
sudo nvidia-ctk cdi generate --output=/etc/cdi/nvidia.yaml

nvidia-ctk cdi list
```

3. confirm gpu is available in container:

```
podman run --rm --device nvidia.com/gpu=all --security-opt=label=disable ubuntu nvidia-smi -L
```

4. run tensorflow container (should not display error that no gpu was found):

```
podman run -it \
           --rm \
           --device nvidia.com/gpu=all \
           --security-opt=label=disable \
           nvcr.io/nvidia/tensorflow:23.10-tf2-py3 \
           nvidia-smi -L
```
5. build custom container image with deepface installed

```
./create_base_dev_image.sh
```

6. test base image

```
podman run -it \
           --rm \
           --device nvidia.com/gpu=all \
           --security-opt=label=disable \
           --volume ~/git/maw-face-recognition/src/deepface:/mnt/scripts \
           --volume ~/maw_face_recognition/deepface/face_db \
           localhost/maw-facerec:latest \
           python /mnt/scripts/test.py
```
