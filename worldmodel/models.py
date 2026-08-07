"""
worldmodel/models.py

Core data models for the Shared World Model.

These classes represent the agent's internal knowledge of the world.

They contain NO reasoning logic.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ==========================================================
# Room
# ==========================================================

@dataclass(slots=True)
class Room:
    """
    Represents a discovered room.
    """

    name: str

    description: str = ""

    exits: dict[str, str] = field(default_factory=dict)

    visited: bool = False


# ==========================================================
# Entity
# ==========================================================

@dataclass(slots=True)
class Entity:
    """
    Generic world entity.

    Examples:
        Silver Key
        Refrigerator
        North Door
        Laptop
        Bottle
    """

    name: str

    category: str

    location: str | None = None

    visible: bool = True


# ==========================================================
# Property
# ==========================================================

@dataclass(slots=True)
class Property:
    """
    Property attached to an entity.

    Examples:

    North Door
        locked=True

    Refrigerator
        open=False
    """

    entity: str

    name: str

    value: object


# ==========================================================
# Relation
# ==========================================================

@dataclass(slots=True)
class Relation:
    """
    Relationship between two entities.

    Examples:

    Silver Key
        on
        Table

    Bottle
        inside
        Refrigerator
    """

    source: str

    relation: str

    target: str


# ==========================================================
# Agent State
# ==========================================================

@dataclass(slots=True)
class AgentState:
    """
    Current state of the agent.
    """

    current_room: str = ""

    inventory: list[str] = field(default_factory=list)

    previous_action: str = ""

    steps_taken: int = 0


# ==========================================================
# World State
# ==========================================================

@dataclass(slots=True)
class WorldState:
    """
    Entire world known by the agent.

    This is the single source of truth for reasoning.
    """

    rooms: dict[str, Room] = field(default_factory=dict)

    entities: dict[str, Entity] = field(default_factory=dict)

    properties: list[Property] = field(default_factory=list)

    relations: list[Relation] = field(default_factory=list)

    agent: AgentState = field(default_factory=AgentState)