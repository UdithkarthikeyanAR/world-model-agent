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
    Expanded demo world.

    Commit 1:
    - Multiple connected rooms
    - World graph
    - Existing API preserved

    Future commits will add:
    - More items
    - Containers
    - Doors
    - Locks
    - Keys
    """

    rooms = {

        # --------------------------------------------------
        # Kitchen
        # --------------------------------------------------

        "kitchen": Room(
            name="Kitchen",
            description="A clean kitchen with a wooden table.",
            exits={
                "south": "hallway",
            },
        ),

        # --------------------------------------------------
        # Hallway
        # --------------------------------------------------

        "hallway": Room(
            name="Hallway",
            description="A hallway connecting several rooms.",
            exits={
                "north": "kitchen",
                "east": "living_room",
                "west": "bedroom",
                "south": "study",
            },
        ),

        # --------------------------------------------------
        # Living Room
        # --------------------------------------------------

        "living_room": Room(
            name="Living Room",
            description="A comfortable living room with a sofa.",
            exits={
                "west": "hallway",
                "east": "garage",
            },
        ),

        # --------------------------------------------------
        # Garage
        # --------------------------------------------------

        "garage": Room(
            name="Garage",
            description="A dusty garage with old tools.",
            exits={
                "west": "living_room",
                "east": "storage",
            },
        ),

        # --------------------------------------------------
        # Storage
        # --------------------------------------------------

        "storage": Room(
            name="Storage Room",
            description="A cluttered storage room.",
            exits={
                "west": "garage",
            },
        ),

        # --------------------------------------------------
        # Bedroom
        # --------------------------------------------------

        "bedroom": Room(
            name="Bedroom",
            description="A quiet bedroom with a neatly made bed.",
            exits={
                "east": "hallway",
                "south": "bathroom",
            },
        ),

        # --------------------------------------------------
        # Bathroom
        # --------------------------------------------------

        "bathroom": Room(
            name="Bathroom",
            description="A small bathroom.",
            exits={
                "north": "bedroom",
            },
        ),

        # --------------------------------------------------
        # Study
        # --------------------------------------------------

        "study": Room(
            name="Study",
            description="A peaceful study filled with books.",
            exits={
                "north": "hallway",
            },
        ),
    }

    # ------------------------------------------------------
    # Items (Commit 1 - keep minimal)
    # ------------------------------------------------------

    items = [

        Item(
            name="Silver Key",
            location="kitchen",
        ),

    ]

    # ------------------------------------------------------
    # Doors (Commit 1 - keep existing)
    # ------------------------------------------------------

    doors = [

        Door(
            name="North Door",
            room="kitchen",
            locked=True,
        ),

    ]

    # ------------------------------------------------------
    # Containers (Commit 1 - keep existing)
    # ------------------------------------------------------

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