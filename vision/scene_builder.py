"""
vision/scene_builder.py

Builds a structured world model from
tracked objects.

Output contains:
- Objects
- Relations
- Summary
"""

from __future__ import annotations

from datetime import datetime

from vision.relationship_engine import RelationshipEngine


class SceneBuilder:

    def __init__(self):

        self.relationship_engine = RelationshipEngine()

    # --------------------------------------------------

    def build(self, tracker):

        world = {

            "timestamp": datetime.now().isoformat(),

            "frame": tracker.frame,

            "summary": {

                "visible_objects": 0,

                "hidden_objects": 0,

                "confirmed_objects": 0,

                "likely_objects": 0,

                "uncertain_objects": 0,

            },

            "objects": [],

            "relations": []

        }

        # ------------------------------------------
        # Objects
        # ------------------------------------------

        for obj in tracker.world_model():

            world["objects"].append({

                "name": obj["object"],

                "status": obj["status"],

                "visible": obj["visible"],

                "confidence": obj["confidence"],

                "bbox": obj["bbox"],

                "first_seen": obj["first_seen"],

                "last_seen": obj["last_seen"],

                "missed_frames": obj["missed_frames"],

            })

            if obj["visible"]:
                world["summary"]["visible_objects"] += 1
            else:
                world["summary"]["hidden_objects"] += 1

            if obj["status"] == "Confirmed":
                world["summary"]["confirmed_objects"] += 1

            elif obj["status"] == "Likely":
                world["summary"]["likely_objects"] += 1

            else:
                world["summary"]["uncertain_objects"] += 1

        # ------------------------------------------
        # Relationships
        # ------------------------------------------

        world["relations"] = self.relationship_engine.build(
            world["objects"]
        )

        return world