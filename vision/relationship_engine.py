"""
vision/relationship_engine.py

Infers simple spatial relationships between
detected objects using their bounding boxes.
"""

from math import sqrt


class RelationshipEngine:

    def build(self, objects):

        relations = []

        for i in range(len(objects)):

            for j in range(i + 1, len(objects)):

                a = objects[i]
                b = objects[j]

                relation = self._infer(a, b)

                if relation is not None:
                    relations.append(relation)

        return relations

    # --------------------------------------------------

    def _infer(self, a, b):

        ax1, ay1, ax2, ay2 = a["bbox"]
        bx1, by1, bx2, by2 = b["bbox"]

        acx = (ax1 + ax2) / 2
        acy = (ay1 + ay2) / 2

        bcx = (bx1 + bx2) / 2
        bcy = (by1 + by2) / 2

        dx = bcx - acx
        dy = bcy - acy

        distance = sqrt(dx * dx + dy * dy)

        if distance < 200:

            return {
                "subject": a["name"],
                "relation": "near",
                "object": b["name"],
            }

        if abs(dx) > abs(dy):

            if dx > 0:

                return {
                    "subject": a["name"],
                    "relation": "left_of",
                    "object": b["name"],
                }

            return {
                "subject": a["name"],
                "relation": "right_of",
                "object": b["name"],
            }

        if dy > 0:

            return {
                "subject": a["name"],
                "relation": "above",
                "object": b["name"],
            }

        return {
            "subject": a["name"],
            "relation": "below",
            "object": b["name"],
        }