# https://viso.ai/computer-vision/deepface/

from deepface import DeepFace;

models = [
    "VGG-Face",
    "Facenet",
    "Facenet512",
    "OpenFace",
    "DeepFace",
    "DeepID",
    "ArcFace",
    "Dlib",
    "SFace",
]

backends = [
    'opencv',
    'ssd',
    'dlib',
    'mtcnn',
    'retinaface',
    'mediapipe',
    'yolov8',
    'yunet',
    'fastmtcnn',
]

recognition = DeepFace.find(
    img_path = "/home/mmorano/maw_face_recognition/test_images/2021/category_name/md/Z62_2396.jpg",
    db_path = "/home/mmorano/maw_face_recognition/deepface/face_db",
    model_name = models[4],
    detector_backend = backends[4],
    enforce_detection = False
);

print(recognition[0].values[0][0]);
