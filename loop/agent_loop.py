"""
loop/agent_loop.py

Main coordination loop for the World Model Agent.

Responsibilities:
- Coordinate the WorldStore
- Coordinate the WorldGraph
- Coordinate the WorldUpdater
- Accept parser-generated UpdateEvents

This module should NOT:
- Parse language
- Execute SQL
- Perform planning
"""

from __future__ import annotations

from typing import Iterable

from contracts.schema import (
    UpdateEvent,
    WorldState,
    PlayerState,
)

from worldmodel.store import WorldStore
from worldmodel.graph import WorldGraph
from updater.updater import WorldUpdater


class AgentLoop:
    """
    Coordinates updates to the world model.
    """

    def __init__(
        self,
        db_path: str = "world.db",
    ) -> None:
        """
        Initialize the world model components.
        """

        self.store = WorldStore(db_path)
        self.graph = WorldGraph(self.store)
        self.updater = WorldUpdater(self.store)

    # -------------------------------------------------------
    # Update Processing
    # -------------------------------------------------------

    def process_updates(
        self,
        updates: Iterable[UpdateEvent],
    ) -> None:
        """
        Process parser-generated updates.
        """

        self.updater.apply_updates(updates)

    # -------------------------------------------------------
    # World Queries
    # -------------------------------------------------------

    def world_state(self) -> WorldState:
        """
        Return the current world state.
        """

        return self.store.get_world_state()

    def player_state(self) -> PlayerState:
        """
        Return the current player state.
        """

        return self.store.get_player_state()

    # -------------------------------------------------------
    # Utilities
    # -------------------------------------------------------

    def reset(self) -> None:
        """
        Reset the entire world model.
        """

        self.store.clear_world()

    def close(self) -> None:
        """
        Close the database connection.
        """

        self.store.close()