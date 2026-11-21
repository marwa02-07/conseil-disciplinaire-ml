import cv2
import os
from datetime import datetime

class FaceStorage:
    def __init__(self, base_dir="detected_faces"):
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)

    def save_faces(self, frame, faces):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        saved_files = []

        for i, (x, y, w, h) in enumerate(faces):
            face_img = frame[y:y+h, x:x+w]
            filename = f"face_{timestamp}_{i}.jpg"
            filepath = os.path.join(self.base_dir, filename)

            cv2.imwrite(filepath, face_img)
            saved_files.append(filepath)

        return saved_files
