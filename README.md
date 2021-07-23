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
