from typing import NamedTuple

class TrainingFace(NamedTuple):
    source_image_path: str
    training_face_image_path: str
    key: str
    detect_score: float
    detected_width: int
    detected_height: int
    extracted_width: int
    extracted_height: int
