"""
environment/renderer.py

Converts the current world state into a text observation.

The parser reads ONLY this output.
"""

from __future__ import annotations

from environment.world import World


class WorldRenderer:
    """
    Renders the current world as text.
    """

    def render(self, world: World) -> str:

        room = world.current_room()

        lines: list[str] = []

        # --------------------------------------------------
        # Current room
        # --------------------------------------------------

        lines.append(
            f"You are in the {room.name.lower()}."
        )

        # --------------------------------------------------
        # Items
        # --------------------------------------------------

        for item in world.room_items():
            lines.append(
                f"A {item.name.lower()} is on the wooden table."
            )

        # --------------------------------------------------
        # Containers
        # --------------------------------------------------

        for container in world.room_containers():

            state = "open" if container.opened else "closed"

            lines.append(
                f"The {container.name.lower()} is {state}."
            )

        # --------------------------------------------------
        # Doors
        # --------------------------------------------------

        for door in world.room_doors():

            state = "locked" if door.locked else "unlocked"

            lines.append(
                f"The {door.name.lower()} is {state}."
            )

        # --------------------------------------------------
        # Exits
        # --------------------------------------------------

        exits = ", ".join(
            room.exits.keys()
        )

        if exits:
            lines.append(
                f"Exits: {exits}."
            )

        return "\n".join(lines)