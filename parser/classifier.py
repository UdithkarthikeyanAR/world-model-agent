"""
- Classify statements
- Return deterministic labels
"""

from __future__ import annotations

import re
from enum import Enum


class SegmentType(str, Enum):
    LOCATION = "location"
    RELATION = "relation"
    PROPERTY = "property"
    EXIT = "exit"
    INVENTORY = "inventory"
    STATUS = "status"
    UNKNOWN = "unknown"


class ObservationClassifier:
    """
    observation segmentation ha semantic ha categories ha idhu classify panudhu.
    """

    LOCATION_PATTERNS = [
        r"^you are in",
        r"^you are at",
        r"^current room",
    ]

    EXIT_PATTERNS = [
        r"^exits?",
        r"^available exits?",
    ]

    INVENTORY_PATTERNS = [
        r"^inventory",
        r"^you have",
    ]

    PROPERTY_PATTERNS = [
        r".* is locked",
        r".* is open",
        r".* is closed",
        r".* is on",
        r".* is off",
    ]

    RELATION_PATTERNS = [
        r".* on .*",
        r".* inside .*",
        r".* in .*",
        r".* next to .*",
    ]

    STATUS_PATTERNS = [
        r"^score",
        r"^health",
        r"^energy",
    ]

    def classify(self, segment: str) -> SegmentType:
        """
        Classify a single observation segment.
        """

        text = segment.strip().lower()

        for pattern in self.LOCATION_PATTERNS:
            if re.match(pattern, text):
                return SegmentType.LOCATION

        for pattern in self.EXIT_PATTERNS:
            if re.match(pattern, text):
                return SegmentType.EXIT

        for pattern in self.INVENTORY_PATTERNS:
            if re.match(pattern, text):
                return SegmentType.INVENTORY

        for pattern in self.PROPERTY_PATTERNS:
            if re.match(pattern, text):
                return SegmentType.PROPERTY

        for pattern in self.RELATION_PATTERNS:
            if re.match(pattern, text):
                return SegmentType.RELATION

        for pattern in self.STATUS_PATTERNS:
            if re.match(pattern, text):
                return SegmentType.STATUS

        return SegmentType.UNKNOWN