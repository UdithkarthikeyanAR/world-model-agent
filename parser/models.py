"""
parser/models.py

Parser-local intermediate data models.

These classes are internal to the Perception layer.

The parser extracts information from observations into these models.
Later, the resolver and updater convert them into canonical
World Model objects defined in contracts/schema.py.

IMPORTANT:
- These classes NEVER contain database IDs.
- They are NEVER stored in SQLite.
- They must remain independent of the World Model implementation.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from contracts.schema import EntityType, RelationType


# ==========================================================
# Parsed Entity
# ==========================================================

@dataclass(slots=True)
class ParsedEntity:
    """
    Entity extracted directly from an observation.

    Example:
        "silver key"
        "wooden table"
        "kitchen"
    """

    name: str
    entity_type: EntityType = EntityType.UNKNOWN


# ==========================================================
# Parsed Relation
# ==========================================================

@dataclass(slots=True)
class ParsedRelation:
    """
    Relation extracted from an observation.

    Example:

        silver key --ON--> wooden table
    """

    source_name: str
    relation: RelationType
    target_name: str


# ==========================================================
# Parsed Property
# ==========================================================

@dataclass(slots=True)
class ParsedProperty:
    """
    Property extracted from an observation.

    Example:

        door:
            locked = True

        lamp:
            power = "on"
    """

    entity_name: str
    key: str
    value: Any


# ==========================================================
# Parsed Observation
# ==========================================================

@dataclass(slots=True)
class ParsedObservation:
    """
    Complete parser output for a single observation.

    This object is passed through:

        Extractor
            ↓
        Resolver
            ↓
        Validator
            ↓
        Updater
    """

    entities: list[ParsedEntity] = field(default_factory=list)

    relations: list[ParsedRelation] = field(default_factory=list)

    properties: list[ParsedProperty] = field(default_factory=list)

    metadata: dict[str, Any] = field(default_factory=dict)

    def is_empty(self) -> bool:
        """
        Returns True if nothing meaningful was extracted.
        """

        return (
            not self.entities
            and not self.relations
            and not self.properties
        )

    def clear(self) -> None:
        """
        Remove all extracted information.
        """

        self.entities.clear()
        self.relations.clear()
        self.properties.clear()
        self.metadata.clear()