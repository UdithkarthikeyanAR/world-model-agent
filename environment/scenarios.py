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
    """
    Represents a movable object in the environment.
    """

    name: str

    # Room name or "inventory"
    location: str

    description: str

    portable: bool = True


@dataclass(slots=True)
class Door:
    name: str
    room: str
    locked: bool = True


@dataclass(slots=True)
class Container:
    """
    A container that can hold items.
    """

    name: str

    room: str

    opened: bool = False

    description: str = ""

    contains: list[str] = field(default_factory=list)


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
        description="A small silver key.",
    ),

    Item(
        name="Cup",
        location="cabinet",
        description="A ceramic coffee cup.",
    ),

    Item(
        name="Book",
        location="living_room",
        description="An old mystery novel.",
    ),

    Item(
        name="Remote",
        location="living_room",
        description="A TV remote.",
    ),

    Item(
        name="Laptop",
        location="desk drawer",
        description="A modern laptop.",
    ),

    Item(
        name="Backpack",
        location="closet",
        description="A black backpack.",
    ),

    Item(
        name="Flashlight",
        location="tool chest",
        description="A bright flashlight.",
    ),

    Item(
        name="Toolbox",
        location="garage",
        description="A heavy toolbox.",
    ),

    Item(
        name="Golden Key",
        location="storage",
        description="A shiny golden key.",
    ),

    Item(
        name="First Aid Kit",
        location="storage",
        description="A medical kit.",
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
        description="A large refrigerator.",
        contains=["Bottle"],
    ),

    Container(
        name="Cabinet",
        room="kitchen",
        opened=False,
        description="A wooden cabinet.",
        contains=["Cup"],
    ),

    Container(
        name="Closet",
        room="bedroom",
        opened=False,
        description="A bedroom closet.",
        contains=["Backpack"],
    ),

    Container(
        name="Desk Drawer",
        room="study",
        opened=False,
        description="A wooden desk drawer.",
        contains=["Laptop"],
    ),

    Container(
        name="Tool Chest",
        room="garage",
        opened=False,
        description="A large tool chest.",
        contains=["Flashlight"],
    ),
]

    return Scenario(
        rooms=rooms,
        items=items,
        doors=doors,
        containers=containers,
        player_start="kitchen",
    )