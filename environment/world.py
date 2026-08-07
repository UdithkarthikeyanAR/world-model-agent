"""
environment/world.py

Maintains the current state of the text world.

The world is loaded from a Scenario and changes as the
agent performs actions.
"""

from __future__ import annotations

from environment.scenarios import (
    Scenario,
    kitchen_demo,
)


class World:
    """
    Represents the current game world.
    """

    def __init__(self, scenario: Scenario | None = None) -> None:

        if scenario is None:
            scenario = kitchen_demo()

        self.scenario = scenario

        # Current player location
        self.player_room = scenario.player_start

        # Inventory starts empty
        self.inventory: list[str] = []

    # ---------------------------------------------------------
    # Room
    # ---------------------------------------------------------

    def current_room(self):
        """
        Return the current room object.
        """

        return self.scenario.rooms[self.player_room]

    # ---------------------------------------------------------
    # Items
    # ---------------------------------------------------------

    def room_items(self) -> list:
        """
        Return items currently in the player's room.
        """

        return [
            item
            for item in self.scenario.items
            if item.location == self.player_room
        ]
    
    def container_items(
        self,
        container_name: str,
    ) -> list:
        """
        Return all items stored inside a container.
        """

        return [

            item

            for item in self.scenario.items

            if item.location.lower() == container_name.lower()

        ]

    # ---------------------------------------------------------
    # Doors
    # ---------------------------------------------------------

    def room_doors(self) -> list:
        """
        Return doors in the player's room.
        """

        return [
            door
            for door in self.scenario.doors
            if door.room == self.player_room
        ]

    # ---------------------------------------------------------
    # Containers
    # ---------------------------------------------------------

    def room_containers(self) -> list:
        """
        Return containers in the player's room.
        """

        return [
            container
            for container in self.scenario.containers
            if container.room == self.player_room
        ]