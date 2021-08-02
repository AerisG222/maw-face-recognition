import os
import cv2
import math
import uuid
import pandas as pd
from retinaface import RetinaFace
from training_face import TrainingFace

image_dir = '/real_images/2021/'
image_size_to_scan = 'lg'
min_dimension = 420
resize_dimension = 299  # (299, 299, 3) is expected shape for Xception
output_dir = '/maw/faces_for_training'

def extract_training_faces_in_directory(dir, files):
    face_results = []

    for file in files:
        image_path = os.path.join(dir, file)
        face_results += extract_training_faces_in_file(image_path)

    return face_results

def get_square_face(img, top, bottom, left, right):
    width = abs(right - left)
    height = abs(top - bottom)

    if(width > height):
        diff = width - height
        top -= math.floor(diff / 2)
        bottom = top + width
    elif(height > width):
        diff = height - width
        left -= math.floor(diff / 2)
        right = left + height

    if(top < 0 or left < 0):
        return ([], None, None, None, None)

    face_image = img[top:bottom, left:right]
    resized_image = cv2.resize(face_image, (resize_dimension,  resize_dimension))

    return (resized_image, top, bottom, left, right)

def extract_training_faces_in_file(image_path):
    face_results = []
    faces = RetinaFace.detect_faces(image_path)

    print(f'  - {os.path.basename(image_path)}', flush = True)

    if type(faces) == dict:
        img = []

        for key in faces:
            face_info = faces[key]
            left, top, right, bottom = face_info['facial_area']
            width = abs(right - left);
            height = abs(bottom - top);

            if width < min_dimension and height < min_dimension:
                continue

            print(f'    - processing {key}: width: {width}, height: {height}')

            if len(img) == 0:
                img = cv2.imread(image_path)

            face_img, new_top, new_bottom, new_left, new_right = get_square_face(img, top, bottom, left, right)

            if(len(face_img) == 0):
                continue

            filename = str(uuid.uuid4()) + '.jpg'
            outfile = os.path.join(output_dir, filename)
            cv2.imwrite(outfile, face_img)
            face_results += TrainingFace(
                image_path,
                outfile,
                key,
                face_info['score'],
                width,
                height,
                abs(new_right - new_left),
                abs(new_top - new_bottom)
            )

    return face_results

def get_report_filename(dir):
    filename = dir[1:].replace('/', '_') + '.csv'

    return os.path.join(output_dir, filename)

def main():
    df = pd.DataFrame()

    for root, dirs, files in os.walk(image_dir):
        if not root.endswith(image_size_to_scan):
            continue

        print(f'*** scanning [{root}]... ***', flush = True)

        face_details = extract_training_faces_in_directory(root, files)
        df = df.append(pd.DataFrame(face_details))

    outfile = os.path.join(output_dir, '_report.csv')
    df.to_csv(outfile, index_label = 'id')

if __name__ == "__main__":
    main()
