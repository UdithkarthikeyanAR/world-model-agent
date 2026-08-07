"""
environment/engine.py

Runs the text world environment.

This module connects:

World
↓
Renderer
↓
Actions
"""

from __future__ import annotations

from environment.world import World
from environment.renderer import WorldRenderer
from environment.actions import WorldActions


class EnvironmentEngine:
    """
    Coordinates the environment.
    """

    def __init__(self) -> None:

        self.world = World()
        self.renderer = WorldRenderer()
        self.actions = WorldActions()

    # ---------------------------------------------------------
    # Observation
    # ---------------------------------------------------------

    def observe(self) -> str:
        """
        Return the current observation.
        """

        return self.renderer.render(self.world)

    # ---------------------------------------------------------
    # Reset
    # ---------------------------------------------------------

    def reset(self) -> None:
        """
        Reset the environment.
        """

        self.world = World()

    # ---------------------------------------------------------
    # Execute
    # ---------------------------------------------------------

    def execute(self, action: str) -> bool:
        """
        Execute an action.

        Supported examples:

        take silver key
        drop silver key

        open refrigerator
        unlock north door

        move north
        move south
        move east
        move west
        """

        action = action.lower().strip()

        # ---------------- Take ----------------

        if action.startswith("take "):

            item = action[5:]

            return self.actions.take_item(
                self.world,
                item,
            )

        # ---------------- Drop ----------------

        if action.startswith("drop "):

            item = action[5:]

            return self.actions.drop_item(
                self.world,
                item,
            )

        # ---------------- Open ----------------

        if action.startswith("open "):

            container = action[5:]

            return self.actions.open_container(
                self.world,
                container,
            )

        # ---------------- Unlock ----------------

        if action.startswith("unlock "):

            door = action[7:]

            return self.actions.unlock_door(
                self.world,
                door,
            )

        # ---------------- Move ----------------

        if action.startswith("move "):

            direction = action[5:]

            return self.actions.move(
                self.world,
                direction,
            )

        return False