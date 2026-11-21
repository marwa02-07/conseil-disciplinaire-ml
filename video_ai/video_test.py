import cv2
import os
import time

from face_detector import FaceDetector
from face_storage import FaceStorage
from violence_detector import ViolenceDetector

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Face detection model path
model_path = os.path.join(
    BASE_DIR,
    "models",
    "haarcascade_frontalface_default.xml"
)

# Initialize detectors
face_detector = FaceDetector(model_path)
violence_detector = ViolenceDetector()

# Face storage
storage = FaceStorage(base_dir=os.path.join(BASE_DIR, "detected_faces"))

# Webcam
cap = cv2.VideoCapture(0)

# Cooldown to avoid duplicate face saving (seconds)
SAVE_COOLDOWN = 3
last_save_time = 0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # -----------------------------
    # FACE DETECTION
    # -----------------------------
    faces = face_detector.detect_faces(frame)

    for (x, y, w, h) in faces:
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (255, 0, 0),
            2
        )

    # Save faces with cooldown
    current_time = time.time()
    if len(faces) > 0 and (current_time - last_save_time) > SAVE_COOLDOWN:
        saved = storage.save_faces(frame, faces)
        print(f"Saved faces: {saved}")
        last_save_time = current_time

    # -----------------------------
    # VIOLENCE DETECTION
    # -----------------------------
    violence, motion_ratio = violence_detector.detect_violence(frame)

    if violence:
        cv2.putText(
            frame,
            "VIOLENCE DETECTED!",
            (30, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 0, 255),
            3
        )

    # -----------------------------
    # DISPLAY
    # -----------------------------
    cv2.imshow("Face & Violence Detection", frame)

    # ESC key to exit
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
