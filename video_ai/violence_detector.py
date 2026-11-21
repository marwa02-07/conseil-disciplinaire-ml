import cv2
import numpy as np
from collections import deque

class ViolenceDetector:
    def __init__(self, history=5, area_ratio=0.05):
        self.prev_gray = None
        self.motion_history = deque(maxlen=history)
        self.area_ratio = area_ratio

    def detect_violence(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.prev_gray is None:
            self.prev_gray = gray
            return False, 0

        diff = cv2.absdiff(self.prev_gray, gray)
        _, thresh = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)

        motion_pixels = cv2.countNonZero(thresh)
        frame_area = frame.shape[0] * frame.shape[1]
        motion_ratio = motion_pixels / frame_area

        self.motion_history.append(motion_ratio)
        avg_motion = sum(self.motion_history) / len(self.motion_history)

        self.prev_gray = gray

        violence = avg_motion > self.area_ratio
        return violence, avg_motion
