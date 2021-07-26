import os
import cv2
from retinaface import RetinaFace
from deepface import DeepFace

dir_known_faces = '/facedb'
dir_image_root = '/facetests'
dir_unknown_faces = '/faces_unkown'

#detection_models = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface']
recognition_models = ['VGG-Face', 'Facenet', 'Facenet512', 'OpenFace', 'DeepFace', 'DeepID', 'ArcFace', 'Dlib']

#detector = detection_models[4]
recognizer = recognition_models[6]

recognizer_model = DeepFace.build_model(recognizer)

def build_unknown_filename(filename, facenum):
    unk = filename \
        .replace('/', '_') \
        .replace('.jpg', f'_{facenum}.jpg') \
        [1:]

    return os.path.join(dir_unknown_faces, unk)

def main():
    for root, dirs, files in os.walk(dir_image_root):
        for file in files:
            imgfile = os.path.join(root, file)

            print(f'Processing {imgfile}...')

            faces = RetinaFace.extract_faces(imgfile)

            print(f'  - found {len(faces)} face(s)')

            i = 1

            for face in faces:
                print(f'  - trying to identify face {i}')

                found_face = DeepFace.find(face, '/facedb', model = recognizer_model, enforce_detection = False)

                if len(found_face) == 0:
                    unk = build_unknown_filename(imgfile, i)
                    cv2.imwrite(unk, face)

                i = i + 1

main()
