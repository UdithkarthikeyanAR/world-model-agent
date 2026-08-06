"""
environment/engine.py

Runs the text world environment.

This module connects:
    World
        ↓
    Renderer
        ↓
    Actions

Parser integration will be added later.
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

    def observe(self) -> str:
        """
        Return the current observation.
        """

        return self.renderer.render(self.world)

    # ---------------------------------------------------------

    def execute(self, action: str) -> bool:
        """
        Execute a simple action.

        Supported actions:
            take key
            open refrigerator
            unlock north door
            move south
            move north
        """

        action = action.lower().strip()

        if action == "take key":
            return self.actions.take_item(
                self.world,
                "Silver Key",
            )

        if action == "open refrigerator":
            return self.actions.open_container(
                self.world,
                "Refrigerator",
            )

        if action == "unlock north door":
            return self.actions.unlock_door(
                self.world,
                "North Door",
            )

        if action.startswith("move "):

            direction = action.split(maxsplit=1)[1]

            return self.actions.move(
                self.world,
                direction,
            )

        return False