"""
vision/detector.py

YOLO object detector.
"""

from ultralytics import YOLO


class ObjectDetector:

    def __init__(self):

        # Nano model (fastest on CPU)
        self.model = YOLO("yolov8n.pt")

    def detect(self, frame):

        return self.model(frame, verbose=False)