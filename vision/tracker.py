"""
vision/tracker.py

Persistent World Memory

Stores detected objects across frames.
Objects remain in memory even if they
temporarily disappear.

Tracks:
- confidence
- bounding box
- visibility
- first/last seen
- missed frames
"""

from __future__ import annotations


class ObjectTracker:

    def __init__(self):

        self.frame = 0

        self.objects = {}

        self.max_missing = 30

    # --------------------------------------------------

    def update(self, detections):

        self.frame += 1

        detected = set()

        # ------------------------------------------
        # Update detected objects
        # ------------------------------------------

        for detection in detections:

            name = detection["name"]

            confidence = detection["confidence"]

            bbox = detection["bbox"]

            detected.add(name)

            if name not in self.objects:

                self.objects[name] = {

                    "confidence": confidence,

                    "bbox": bbox,

                    "first_seen": self.frame,

                    "last_seen": self.frame,

                    "missed_frames": 0,

                    "visible": True,

                }

            else:

                obj = self.objects[name]

                # Smooth confidence over time
                obj["confidence"] = (
                    obj["confidence"] * 0.7 +
                    confidence * 0.3
                )

                # Update latest bounding box
                obj["bbox"] = bbox

                obj["last_seen"] = self.frame

                obj["missed_frames"] = 0

                obj["visible"] = True

        # ------------------------------------------
        # Handle missing objects
        # ------------------------------------------

        remove = []

        for name, obj in self.objects.items():

            if name not in detected:

                obj["missed_frames"] += 1

                if obj["missed_frames"] > 5:

                    obj["visible"] = False

                if obj["missed_frames"] > self.max_missing:

                    remove.append(name)

        for name in remove:

            del self.objects[name]

    # --------------------------------------------------

    def world_model(self):

        world = []

        for name, obj in sorted(self.objects.items()):

            confidence = obj["confidence"]

            if confidence >= 0.80:
                status = "Confirmed"

            elif confidence >= 0.50:
                status = "Likely"

            else:
                status = "Uncertain"

            world.append({

                "object": name,

                "status": status,

                "confidence": round(confidence, 2),

                "bbox": obj["bbox"],

                "visible": obj["visible"],

                "first_seen": obj["first_seen"],

                "last_seen": obj["last_seen"],

                "missed_frames": obj["missed_frames"],

            })

        return world