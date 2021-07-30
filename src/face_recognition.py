import os
import cv2
import pandas as pd
from deepface import DeepFace
from retinaface import RetinaFace
from retinaface.commons import postprocess
from face_info import FaceInfo

dir_known_faces = '/face_db'
dir_found_faces = '/faces_found'
dir_unknown_faces = '/faces_unknown'
dir_test_images = '/test_images'
dir_real_images = '/real_images/2021/memorial_day'

# test/live toggle
dir_image_root = dir_real_images


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
            left, top, right, bottom = face_info['facial_area']
            face_img = img[top:bottom, left:right]
            face_info['aligned_face'] = align_face_image(face_info, face_img)

    return faces

def get_person_name_from_file(known_face_path):
    return known_face_path.split('/')[-2].replace('_', ' ')

def find_faces_in_directory(dir, files):
    face_results = []

    for file in files:
        image_path = os.path.join(dir, file)
        face_results += find_faces_in_file(image_path)

    return face_results

def find_faces_in_file(image_path):
    face_results = []
    print(f'Processing {image_path}...', flush = True)
    faces = get_aligned_faces_in_image(image_path)
    print(f'  - found {len(faces)} face(s)', flush = True)
    face_results += get_face_details(image_path, faces)

    return face_results

def get_face_details(image_path, aligned_faces):
    face_results = []

    for key in aligned_faces:
        if len(key) == 0:
            print('  - invalid face - skipping')
            continue

        print(f'  - trying to identify face {key}', flush = True)
        current_face = aligned_faces[key]
        face_image = current_face['aligned_face']
        found_face = DeepFace.find(face_image, dir_known_faces, model = recognizer_model, model_name = recognizer, enforce_detection = False)

        recognized_person_db_file = ''
        recognized_person_distance = None
        recognized_person_name = ''

        if len(found_face) > 0:
            recognized_person_db_file = found_face.iloc[0,0]
            recognized_person_distance = found_face.iloc[0,1]
            recognized_person_name = get_person_name_from_file(recognized_person_db_file)
        else:
            unk = build_unknown_filename(image_path, key)
            cv2.imwrite(unk, face_image)

        height, width, channels = cv2.imread(image_path).shape
        face_left, face_top, face_right, face_bottom = current_face['facial_area']
        face_results.append(FaceInfo(
            image_path,
            width,
            height,
            face_top,
            face_bottom,
            face_left,
            face_right,
            current_face['score'],
            recognized_person_db_file,
            recognized_person_distance,
            recognized_person_name,
            len(recognized_person_name) > 0
        ))

    return face_results

def get_report_filename(dir):
    filename = dir[1:].replace('/', '_') + '.csv'

    return os.path.join(dir_found_faces, filename)

def main():
    for root, dirs, files in os.walk(dir_image_root):
        if not root.endswith('md'):
            continue

        print(f'*** [{root}] ***', flush = True)
        face_details = find_faces_in_directory(root, files)
        df = pd.DataFrame(face_details)
        outfile = get_report_filename(root)
        df.to_csv(outfile, index_label = 'id')

recognizer = 'ArcFace'
recognizer_model = DeepFace.build_model(recognizer)

main()
