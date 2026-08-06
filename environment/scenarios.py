"""
environment/scenarios.py

Contains predefined demo worlds for the World Model Agent.

Each scenario is a lightweight description of the environment.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# ==========================================================
# Basic Objects
# ==========================================================

@dataclass(slots=True)
class Room:
    name: str
    description: str
    exits: dict[str, str] = field(default_factory=dict)


@dataclass(slots=True)
class Item:
    name: str
    location: str


@dataclass(slots=True)
class Door:
    name: str
    room: str
    locked: bool = True


@dataclass(slots=True)
class Container:
    name: str
    room: str
    opened: bool = False


# ==========================================================
# Scenario
# ==========================================================

@dataclass(slots=True)
class Scenario:
    rooms: dict[str, Room]
    items: list[Item]
    doors: list[Door]
    containers: list[Container]
    player_start: str


# ==========================================================
# Demo Scenario
# ==========================================================

def kitchen_demo() -> Scenario:
    """
    Simple demo world used during evaluation.
    """

    rooms = {

        "kitchen": Room(
            name="kitchen",
            description="A clean kitchen with a wooden table.",
            exits={
                "south": "hallway",
            },
        ),

        "hallway": Room(
            name="Hallway",
            description="A narrow hallway.",
            exits={
                "north": "kitchen",
            },
        ),
    }

    items = [

        Item(
            name="Silver Key",
            location="kitchen",
        ),

    ]

    doors = [

        Door(
            name="North Door",
            room="kitchen",
            locked=True,
        ),

    ]

    containers = [

        Container(
            name="Refrigerator",
            room="kitchen",
            opened=False,
        ),

    ]

    return Scenario(
        rooms=rooms,
        items=items,
        doors=doors,
        containers=containers,
        player_start="kitchen",
    )