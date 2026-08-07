"""
environment/actions.py

Applies actions to the world.

These actions modify the world state so that the next
observation is different.
"""

from __future__ import annotations

from environment.world import World


class WorldActions:
    """
    Applies actions to the world.
    """

    # ---------------------------------------------------------
    # Items
    # ---------------------------------------------------------

    def take_item(
        self,
        world: World,
        item_name: str,
    ) -> bool:
        """
        Move a portable item from the room into the inventory.
        """

        for item in world.room_items():

            if item.name.lower() != item_name.lower():
                continue

            # Cannot pick up this object
            if not item.portable:
                return False

            # Already carrying it
            if item.location == "inventory":
                return False

            item.location = "inventory"

            world.inventory.append(item.name)

            return True

        return False

    # ---------------------------------------------------------

    def drop_item(
        self,
        world: World,
        item_name: str,
    ) -> bool:
        """
        Drop an inventory item into the current room.
        """

        for item in world.scenario.items:

            if item.name.lower() != item_name.lower():
                continue

            if item.location != "inventory":
                return False

            item.location = world.player_room

            if item.name in world.inventory:
                world.inventory.remove(item.name)

            return True

        return False

    # ---------------------------------------------------------
    # Containers
    # ---------------------------------------------------------

    def open_container(
        self,
        world: World,
        container_name: str,
    ) -> bool:
        """
        Open a container.
        """

        for container in world.room_containers():

            if container.name.lower() == container_name.lower():

                container.opened = True

                return True

        return False

    # ---------------------------------------------------------
    # Doors
    # ---------------------------------------------------------

    def unlock_door(
        self,
        world: World,
        door_name: str,
    ) -> bool:
        """
        Unlock a door if the player has the Silver Key.
        """

        if "Silver Key" not in world.inventory:
            return False

        for door in world.room_doors():

            if door.name.lower() == door_name.lower():

                door.locked = False

                return True

        return False

    # ---------------------------------------------------------
    # Movement
    # ---------------------------------------------------------

    def move(
        self,
        world: World,
        direction: str,
    ) -> bool:
        """
        Move the player to another room.
        """

        room = world.current_room()

        direction = direction.lower()

        if direction not in room.exits:
            return False

        world.player_room = room.exits[direction]

        return True