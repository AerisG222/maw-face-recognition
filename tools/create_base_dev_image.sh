#!/bin/bash
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

buildah bud -f "${SCRIPT_DIR}/Containerfile" -t maw-facerec "${SCRIPT_DIR}"
