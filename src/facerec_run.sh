#!/bin/bash
pip install face_recognition

face_recognition \
    --show-distance True \
    --tolerance 0.4 \
    /facerec_known_faces \
    /real_images/2021/memorial_day/md
