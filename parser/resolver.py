"""
parser/resolver.py

Normalizes parser output before validation.

Responsibilities
----------------
- Normalize entity names
- Remove duplicate entities
- Remove duplicate relations
- Remove duplicate properties

This module does NOT:
- assign IDs
- access SQLite
- update the world model
"""

from __future__ import annotations

from parser.models import (
    ParsedEntity,
    ParsedObservation,
    ParsedProperty,
    ParsedRelation,
)


class ObservationResolver:
    """
    Resolves duplicate parser outputs and normalizes names.
    """

    def resolve(
        self,
        observation: ParsedObservation,
    ) -> ParsedObservation:
        """
        Normalize a ParsedObservation.
        """

        self._normalize_entities(observation)
        self._deduplicate_entities(observation)
        self._deduplicate_relations(observation)
        self._deduplicate_properties(observation)

        return observation

    # ======================================================
    # Entity normalization
    # ======================================================

    def _normalize_entities(
        self,
        observation: ParsedObservation,
    ) -> None:

        for entity in observation.entities:
            entity.name = entity.name.strip().lower()

    # ======================================================
    # Entity deduplication
    # ======================================================

    def _deduplicate_entities(
        self,
        observation: ParsedObservation,
    ) -> None:

        unique = {}

        for entity in observation.entities:
            unique[entity.name] = entity

        observation.entities = list(unique.values())

    # ======================================================
    # Relation deduplication
    # ======================================================

    def _deduplicate_relations(
        self,
        observation: ParsedObservation,
    ) -> None:

        unique = {}

        for relation in observation.relations:

            key = (
                relation.source_name.lower(),
                relation.relation,
                relation.target_name.lower(),
            )

            unique[key] = relation

        observation.relations = list(unique.values())

    # ======================================================
    # Property deduplication
    # ======================================================

    def _deduplicate_properties(
        self,
        observation: ParsedObservation,
    ) -> None:

        unique = {}

        for prop in observation.properties:

            key = (
                prop.entity_name.lower(),
                prop.key,
            )

            unique[key] = prop

        observation.properties = list(unique.values())