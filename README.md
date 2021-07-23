# Face Recognition tool for mikeandwan.us photos

## Prep

1. Make sure podman + nvidia drivers are installed
2. Follow post: https://www.quora.com/How-can-TensorFlow-with-NVIDIA-GPU-support-be-installed-on-Fedora-32
3. `tools/test_nvidia_container.sh`
4. Edit /etc/nvidia-container-runtime/config.toml to specify no-cgroups=true
5. step 3 should now indicate permission error
6. `sudo chcon -t container_file_t /dev/nvidia*` to relax selinux
7. step 3 now works!

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
