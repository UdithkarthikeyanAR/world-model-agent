"""
vision/keyframe.py

Keyframe extraction for visual observations.

The current MVP operates on text observations, so this module
acts as a placeholder for future image/video support.

Future responsibilities:
- Select representative frames from video streams.
- Remove near-duplicate frames.
- Prepare frames for visual perception models.
"""

from __future__ import annotations

from typing import Any


class KeyframeExtractor:
    """
    Placeholder keyframe extractor.

    Future implementations may use OpenCV or another vision
    library to identify important frames from video input.
    """

    def __init__(self) -> None:
        pass

    def extract(self, frame: Any) -> Any:
        """
        Return the input frame unchanged.

        Parameters
        ----------
        frame : Any
            Image or video frame.

        Returns
        -------
        Any
            The same frame.
        """
        return frame

    def extract_batch(self, frames: list[Any]) -> list[Any]:
        """
        Placeholder batch processing.

        Parameters
        ----------
        frames : list[Any]
            Collection of frames.

        Returns
        -------
        list[Any]
            Unmodified frames.
        """
        return frames