"""
worldmodel/models.py

Defines the core data models used by the world model.
These models represent the objects stored in the SQLite database.

This module contains no database logic.
"""

from dataclasses import dataclass, field
from typing import Optional, Dict, List
from datetime import datetime

@dataclass(slots=True)
class Entity:
    """
    Represents any object in the world.
    """

    id: int
    name: str
    entity_type: str

@dataclass(slots=True)
class Relation:
    """
    Represents a relationship between two entities.
    """

    source_id: int
    relation: str
    target_id: int

@dataclass(slots=True)
class Property:
    """
    Represents an attribute of an entity.
    """

    entity_id: int
    key: str
    value: str

@dataclass(slots=True)
class PlayerState:
    """
    Represents the player's current state.
    """

    player_id: int
    current_room: int
    inventory: List[int] = field(default_factory=list)

@dataclass(slots=True)
class WorldState:
    """
    Complete in-memory snapshot of the world.
    """

    entities: Dict[int, Entity] = field(default_factory=dict)

    relations: List[Relation] = field(default_factory=list)

    properties: List[Property] = field(default_factory=list)

    player: Optional[PlayerState] = None

@dataclass(slots=True)
class Revision:
    """
    Represents a change made to the world state.
    """

    revision_id: int
    timestamp: datetime
    description: str