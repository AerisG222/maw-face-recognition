#!/bin/bash

# this just runs the python app and kills some unwanted warnings that the deepface library emits
python face_recognition.py | sed '/^WARNING/d; /^Already/d; /^There/d; /^find/d'
