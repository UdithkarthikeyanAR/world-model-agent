"""
parser/validator.py

Validates parser output before it is passed to the updater.

Responsibilities
----------------
- Validate ParsedObservation
- Detect missing entities
- Detect invalid relations
- Detect invalid properties

This module NEVER:
- modifies parser output
- assigns IDs
- accesses SQLite
"""

from __future__ import annotations

from parser.models import ParsedObservation


class ObservationValidator:
    """
    Validates ParsedObservation objects.
    """

    def validate(self, observation: ParsedObservation) -> tuple[bool, list[str]]:
        """
        Validate a ParsedObservation.

        Returns
        -------
        tuple
            (is_valid, list_of_errors)
        """

        errors: list[str] = []

        self._validate_entities(observation, errors)
        self._validate_relations(observation, errors)
        self._validate_properties(observation, errors)

        return len(errors) == 0, errors

    # ======================================================
    # Entity Validation
    # ======================================================

    def _validate_entities(
        self,
        observation: ParsedObservation,
        errors: list[str],
    ) -> None:

        for entity in observation.entities:

            if not entity.name.strip():
                errors.append("Entity name cannot be empty.")

    # ======================================================
    # Relation Validation
    # ======================================================

    def _validate_relations(
        self,
        observation: ParsedObservation,
        errors: list[str],
    ) -> None:

        entity_names = {
            entity.name.lower()
            for entity in observation.entities
        }

        for relation in observation.relations:

            if relation.source_name.lower() not in entity_names:
                errors.append(
                    f"Unknown source entity: '{relation.source_name}'."
                )

            if relation.target_name.lower() not in entity_names:
                errors.append(
                    f"Unknown target entity: '{relation.target_name}'."
                )

    # ======================================================
    # Property Validation
    # ======================================================

    def _validate_properties(
        self,
        observation: ParsedObservation,
        errors: list[str],
    ) -> None:

        entity_names = {
            entity.name.lower()
            for entity in observation.entities
        }

        for prop in observation.properties:

            if prop.entity_name.lower() not in entity_names:
                errors.append(
                    f"Unknown property owner: '{prop.entity_name}'."
                )

            if not prop.key.strip():
                errors.append(
                    f"Property key missing for '{prop.entity_name}'."
                )