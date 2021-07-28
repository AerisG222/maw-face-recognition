from typing import NamedTuple

class FaceInfo(NamedTuple):
    file: str
    image_width: int
    image_height: int
    face_top: int
    face_bottom: int
    face_left: int
    face_right: int
    detect_score: float
    recognizer_match_file: str
    recognizer_distance: float
    person_name: str
    was_identified: bool
