import os
import cv2
from retinaface import RetinaFace
from deepface import DeepFace

detection_models = ["opencv", "ssd", "dlib", "mtcnn", "retinaface"]
recognition_models = ["VGG-Face", "Facenet", "Facenet512", "OpenFace", "DeepFace", "DeepID", "ArcFace", "Dlib"]

detector = detection_models[4]
recognizer = recognition_models[6]

recognizer_model = DeepFace.build_model(recognizer)

for root, dirs, files in os.walk('/facetests'):
    for file in files:
        imgfile = os.path.join(root, file)

        print(f'Processing {imgfile}...')

        faces = RetinaFace.extract_faces(imgfile)

        print(f'  - found {len(faces)} face(s)')

        i = 1

        for face in faces:
            #cv2.imwrite(f'out{i}_{file}', face)
            print(f'  - trying to identify face {i}')

            found_face = DeepFace.find(face, '/facedb', model = recognizer_model, detector_backend = detector, enforce_detection = False)
            print(found_face)

            i = i + 1
