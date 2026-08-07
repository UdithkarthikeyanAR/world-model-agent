"""
shared/world_model.py

Shared World Model

Single source of truth for both
Text and Vision pipelines.

Parser and Vision update this model.

Planner, Rule Engine and ModelClient
only read from this model.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import datetime


class SharedWorldModel:

    def __init__(self):
        self.clear()

    # ---------------------------------------------------------

    def clear(self):

        self.entities = {}
        self.relations = []
        self.properties = {}

        self.metadata = {
            "created": datetime.now().isoformat(),
            "last_updated": None,
            "next_entity_id": 1,
        }

    # ---------------------------------------------------------

    def _new_entity_id(self):

        entity_id = f"entity_{self.metadata['next_entity_id']}"
        self.metadata["next_entity_id"] += 1
        return entity_id

    # ---------------------------------------------------------

    def _find_entity(self, name, source):

        for entity_id, entity in self.entities.items():

            if entity["name"] == name and entity["source"] == source:
                return entity_id

        return None

    # ---------------------------------------------------------
    # TEXT PIPELINE
    # ---------------------------------------------------------

    def update_from_text(self, parsed):

        self.metadata["last_updated"] = datetime.now().isoformat()

        for entity in parsed.entities:

            entity_id = self._find_entity(
                entity.name,
                "text",
            )

            if entity_id is None:
                entity_id = self._new_entity_id()

            self.entities[entity_id] = {
                "id": entity_id,
                "name": entity.name,
                "type": entity.type,
                "source": "text",
            }

        self.relations = []

        for relation in parsed.relations:

            self.relations.append({
                "subject": relation.subject,
                "relation": relation.relation,
                "object": relation.object,
                "source": "text",
            })

        self.properties = {}

        for prop in parsed.properties:

            self.properties.setdefault(
                prop.object,
                {}
            )[prop.name] = prop.value

    # ---------------------------------------------------------
    # VISION PIPELINE
    # ---------------------------------------------------------

    def update_from_vision(self, scene):

        self.metadata["last_updated"] = datetime.now().isoformat()

        # -----------------------------
        # Entities
        # -----------------------------

        for obj in scene["objects"]:

            entity_id = self._find_entity(
                obj["name"],
                "vision",
            )

            if entity_id is None:
                entity_id = self._new_entity_id()

            self.entities[entity_id] = {

                "id": entity_id,
                "name": obj["name"],
                "type": "vision_object",
                "source": "vision",

                "visible": obj["visible"],
                "confidence": obj["confidence"],
                "status": obj["status"],
                "bbox": obj["bbox"],

                "first_seen": obj["first_seen"],
                "last_seen": obj["last_seen"],
                "missed_frames": obj["missed_frames"],
            }

        # -----------------------------
        # Relationships
        # -----------------------------

        self.relations = []

        for relation in scene["relations"]:

            self.relations.append({

                "subject": relation["subject"],
                "relation": relation["relation"],
                "object": relation["object"],
                "source": "vision",

            })

        # -----------------------------
        # Metadata
        # -----------------------------

        self.metadata["frame"] = scene["frame"]
        self.metadata["timestamp"] = scene["timestamp"]
        self.metadata["summary"] = scene["summary"]

    # ---------------------------------------------------------

    def add_relation(
        self,
        subject,
        relation,
        object_,
        source="system",
    ):

        self.relations.append({

            "subject": subject,
            "relation": relation,
            "object": object_,
            "source": source,

        })

    # ---------------------------------------------------------

    def get_entity(self, entity_id):

        return deepcopy(
            self.entities.get(entity_id)
        )

    # ---------------------------------------------------------

    def find_by_name(self, name):

        return [

            deepcopy(entity)

            for entity in self.entities.values()

            if entity["name"] == name

        ]

    # ---------------------------------------------------------

    def get_entities(self):

        return deepcopy(
            list(self.entities.values())
        )

    # ---------------------------------------------------------

    def get_relations(self):

        return deepcopy(
            self.relations
        )

    # ---------------------------------------------------------

    def get_properties(self):

        return deepcopy(
            self.properties
        )

    # ---------------------------------------------------------

    def summary(self):

        return {

            "entities": len(self.entities),
            "relations": len(self.relations),
            "properties": len(self.properties),

        }

    # ---------------------------------------------------------

    def export(self):

        return {

            "entities": deepcopy(
                list(self.entities.values())
            ),

            "relations": deepcopy(
                self.relations
            ),

            "properties": deepcopy(
                self.properties
            ),

            "metadata": deepcopy(
                self.metadata
            ),

        }