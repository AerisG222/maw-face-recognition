from retinaface import RetinaFace
import cv2
import os

test_path = '/test_images/2021/category_name/md'
test_img = os.path.join(test_path, 'Z62_2396.jpg')
img = cv2.imread(test_img)
obj = RetinaFace.detect_faces(test_img)

for key in obj.keys():
    identity = obj[key]

    facial_area = identity["facial_area"]

    print(facial_area)

    cv2.rectangle(img, (facial_area[2], facial_area[3]), (facial_area[0], facial_area[1]), (255, 255, 255), 1)

    left = facial_area[0]
    top = facial_area[1]
    right = facial_area[2] + 1
    bottom = facial_area[3] + 1

    faceimg = img[top:bottom, left:right]
    cv2.imwrite(os.path.join(test_path, f'face_detect_result_{key}.jpg'), faceimg)

cv2.imwrite(os.path.join(test_path, 'face_detect_result.jpg'), img)

