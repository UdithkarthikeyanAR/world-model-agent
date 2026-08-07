"""
parser/extractor.py

Extracts structured parser-local objects from classified observation
segments.

inda module NEVER:
- assigns IDs
- updates the database
- resolves duplicates
- creates World Model entities
"""


from __future__ import annotations
from re import match

import re

from contracts.schema import EntityType, RelationType

from parser.classifier import SegmentType
from parser.models import (
    ParsedEntity,
    ParsedObservation,
    ParsedProperty,
    ParsedRelation,
)


class ObservationExtractor:
    """
    Converts classified observation segments into parser-local models.
    """

    def extract(
        self,
        segment: str,
        segment_type: SegmentType,
    ) -> ParsedObservation:
        """
        Main extraction entry point.
        """

        observation = ParsedObservation()

        match segment_type:

            case SegmentType.LOCATION:
                self._extract_location(segment, observation)

            case SegmentType.RELATION:
                self._extract_relation(segment, observation)

            case SegmentType.PROPERTY:
                self._extract_property(segment, observation)

            case _:
                pass
        self._extract_item(segment, observation)
        return observation

    # ======================================================
    # LOCATION
    # ======================================================

    def _extract_location(
        self,
        segment: str,
        observation: ParsedObservation,
    ) -> None:

        match = re.search(
            r"you are (?:in|at) the (.+?)[.]?$",
            segment,
            re.IGNORECASE,
        )

        if not match:
            return

        room = match.group(1).strip()
        observation.metadata["current_room"] = room.lower()

        observation.entities.append(
            ParsedEntity(
                name=room,
                entity_type=EntityType.ROOM,
            )
        )

    # ======================================================
    # RELATION
    # ======================================================

    def _extract_relation(
        self,
        segment: str,
        observation: ParsedObservation,
    ) -> None:

        patterns = [

            (
                r"(.+?) is on (.+?)[.]?$",
                RelationType.ON,
                EntityType.ITEM,
                EntityType.SURFACE,
            ),

            (
                r"(.+?) is inside (.+?)[.]?$",
                RelationType.INSIDE,
                EntityType.ITEM,
                EntityType.CONTAINER,
            ),

            (
                r"(.+?) is in (.+?)[.]?$",
                RelationType.IN,
                EntityType.ITEM,
                EntityType.ROOM,
            ),
        ]

        for pattern, relation, src_type, dst_type in patterns:

            match = re.search(
                pattern,
                segment,
                re.IGNORECASE,
            )

            if not match:
                continue

            source = match.group(1).strip()
            target = match.group(2).strip()

            observation.entities.append(
                ParsedEntity(
                    name=source,
                    entity_type=src_type,
                )
            )

            observation.entities.append(
                ParsedEntity(
                    name=target,
                    entity_type=dst_type,
                )
            )

            observation.relations.append(
                ParsedRelation(
                    source_name=source,
                    relation=relation,
                    target_name=target,
                )
            )

            return

    # ======================================================
    # PROPERTY
    # ======================================================

    def _extract_property(
        self,
        segment: str,
        observation: ParsedObservation,
    ) -> None:

        patterns = [

            (r"(.+?) is locked[.]?$", "locked", True),

            (r"(.+?) is open[.]?$", "open", True),

            (r"(.+?) is closed[.]?$", "open", False),

            (r"(.+?) is on[.]?$", "power", "on"),

            (r"(.+?) is off[.]?$", "power", "off"),
        ]

        for pattern, key, value in patterns:

            match = re.search(
                pattern,
                segment,
                re.IGNORECASE,
            )

            if not match:
                continue

            entity = match.group(1).strip()

            entity_name = entity.lower()

            entity_type = EntityType.UNKNOWN

            if "door" in entity_name:
                entity_type = EntityType.DOOR
            elif "refrigerator" in entity_name:
                entity_type = EntityType.CONTAINER
            elif "cabinet" in entity_name:
                entity_type = EntityType.CONTAINER

            observation.entities.append(
                ParsedEntity(
                    name=entity,
                    entity_type=entity_type,
                )
            )

            observation.properties.append(
                ParsedProperty(
                    entity_name=entity,
                    key=key,
                    value=value,
                )
            )

            return

    def _extract_item(
        self,
        segment: str,
        observation: ParsedObservation,
    ) -> None:

        match = re.search(
            r"(?:a|an)\s+(.+?)\s+is here[.]?$",
            segment,
            re.IGNORECASE,
        )

        if not match:
            return

        item = match.group(1).strip()

        observation.entities.append(
            ParsedEntity(
                name=item,
                entity_type=EntityType.ITEM,
            )
        )