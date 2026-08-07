"""
vision/video_loader.py

Opens the webcam and returns live frames.
"""

from __future__ import annotations

import cv2


class VideoLoader:
    """
    Webcam video source.
    """

    def __init__(self, camera_index: int = 0) -> None:

        self.capture = cv2.VideoCapture(camera_index)

        if not self.capture.isOpened():
            raise RuntimeError(
                "Unable to open webcam."
            )

    def read(self):
        """
        Read one frame.
        """

        return self.capture.read()

    def release(self):
        """
        Release webcam.
        """

        self.capture.release()