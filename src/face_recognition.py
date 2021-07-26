import os
import cv2
from retinaface import RetinaFace
from deepface import DeepFace
from retinaface.commons import postprocess

dir_known_faces = '/facedb'
dir_image_root = '/facetests'
dir_unknown_faces = '/faces_unkown'


def build_unknown_filename(filename, facenum):
    unk = filename \
        .replace('/', '_') \
        .replace('.jpg', f'_{facenum}.jpg') \
        [1:]

    return os.path.join(dir_unknown_faces, unk)

def align_face_image(face_info, face_image):
    landmarks = face_info['landmarks']
    left_eye = landmarks['left_eye']
    right_eye = landmarks['right_eye']
    nose = landmarks['nose']
    mouth_right = landmarks['mouth_right']
    mouth_left = landmarks['mouth_left']

    return postprocess.alignment_procedure(face_image, right_eye, left_eye)

# adapted from extract_faces at https://github.com/serengil/retinaface/blob/master/retinaface/RetinaFace.py
def get_aligned_faces_in_image(filename):
    faces = RetinaFace.detect_faces(filename)
    img = cv2.imread(filename)

    if type(faces) == dict:
        for key in faces:
            face_info = faces[key]
            facial_area = face_info['facial_area']
            face_img = img[facial_area[1]: facial_area[3], facial_area[0]: facial_area[2]]
            face_info['aligned_face'] = align_face_image(face_info, face_img)

    return faces

def main():
    #detection_models = ['opencv', 'ssd', 'dlib', 'mtcnn', 'retinaface']
    recognition_models = ['VGG-Face', 'Facenet', 'Facenet512', 'OpenFace', 'DeepFace', 'DeepID', 'ArcFace', 'Dlib']
    #detector = detection_models[4]
    recognizer = recognition_models[6]
    recognizer_model = DeepFace.build_model(recognizer)

    for root, dirs, files in os.walk(dir_image_root):
        for file in files:
            imgfile = os.path.join(root, file)

            print(f'Processing {imgfile}...')

            faces = get_aligned_faces_in_image(imgfile)

            print(f'  - found {len(faces)} face(s)')

            for key in faces:
                print(f'  - trying to identify face {key}')

                faceimg = faces[key]['aligned_face']
                found_face = DeepFace.find(faceimg, '/facedb', model = recognizer_model, model_name = recognizer, enforce_detection = False)

                if len(found_face) == 0:
                    unk = build_unknown_filename(imgfile, key)
                    cv2.imwrite(unk, faceimg)

main()
