"""
contracts/schema.py

Shared data models for the World Model Agent.

Every module should import these classes instead of creating
its own data models.

This file is the canonical schema shared by the entire team.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# ==========================================================
# Entity Types
# ==========================================================

class EntityType(str, Enum):
    ROOM = "room"
    OBJECT = "object"
    PLAYER = "player"
    NPC = "npc"
    CONTAINER = "container"
    SURFACE = "surface"
    DOOR = "door"
    ITEM = "item"
    UNKNOWN = "unknown"


# ==========================================================
# Relation Types
# ==========================================================

class RelationType(str, Enum):
    IN = "in"
    ON = "on"
    INSIDE = "inside"
    CONNECTED_TO = "connected_to"
    HOLDS = "holds"
    OWNS = "owns"
    NEXT_TO = "next_to"
    OPEN = "open"
    CLOSED = "closed"
    UNKNOWN = "unknown"


# ==========================================================
# Entity
# ==========================================================

@dataclass(slots=True)
class Entity:
    """
    Represents any object in the world.
    """

    id: int
    name: str
    entity_type: EntityType


# ==========================================================
# Relation
# ==========================================================

@dataclass(slots=True)
class Relation:
    """
    Represents a graph edge between two entities.
    """

    source_id: int
    relation: RelationType
    target_id: int


# ==========================================================
# Property
# ==========================================================

@dataclass(slots=True)
class Property:
    """
    Represents an attribute attached to an entity.
    """

    entity_id: int
    key: str
    value: Any


# ==========================================================
# Player State
# ==========================================================

@dataclass(slots=True)
class PlayerState:
    """
    Represents the current player state.
    """

    player_id: int
    current_room: int
    inventory: list[int] = field(default_factory=list)


# ==========================================================
# Update Event
# ==========================================================

@dataclass(slots=True)
class UpdateEvent:
    """
    Represents a change requested by the parser.
    """

    entity_id: int
    field: str
    old_value: Any
    new_value: Any
    timestamp: float = 0.0


# ==========================================================
# World State
# ==========================================================

@dataclass(slots=True)
class WorldState:
    """
    Snapshot of the complete world.
    """

    entities: list[Entity] = field(default_factory=list)
    relations: list[Relation] = field(default_factory=list)
    properties: list[Property] = field(default_factory=list)
    player: PlayerState | None = None