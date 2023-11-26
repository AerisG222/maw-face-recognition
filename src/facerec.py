# https://viso.ai/computer-vision/deepface/
import pandas as pd
from deepface import DeepFace

# MODELS
#  - VGG-Face
#  - Facenet
#  - Facenet512
#  - OpenFace
#  - DeepFace
#  - DeepID
#  - ArcFace
#  - Dlib
#  - SFace

# DETECTORS
#  - opencv
#  - ssd
#  - dlib
#  - mtcnn
#  - retinaface
#  - mediapipe
#  - yolov8
#  - yunet
#  - fastmtcnn

def recognizeFaces(inputImage, faceDbDir):
    return pd.concat(
        DeepFace.find(
            img_path = inputImage,
            db_path = faceDbDir,
            model_name = "Facenet512",
            detector_backend = "mtcnn",
            enforce_detection = False
        )
    )
