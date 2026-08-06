"""
decision/planner.py

Generates possible actions from the current WorldSlice.

The planner does NOT execute actions.
It only proposes valid actions.
"""

from __future__ import annotations

from dataclasses import dataclass

from contracts.schema import Entity
from query.slice_builder import WorldSlice


@dataclass(slots=True)
class PlannedAction:
    """
    Represents one possible action.
    """

    action: str
    target: Entity | None = None


class Planner:
    """
    Generates candidate actions from a WorldSlice.
    """

    def plan(self, world_slice: WorldSlice) -> list[PlannedAction]:

        actions: list[PlannedAction] = []

        # Visible entities
        for entity in world_slice.visible_entities:

            actions.append(
                PlannedAction(
                    action="inspect",
                    target=entity,
                )
            )

            actions.append(
                PlannedAction(
                    action="interact",
                    target=entity,
                )
            )

        # Inventory items
        for item in world_slice.inventory:

            actions.append(
                PlannedAction(
                    action="use",
                    target=item,
                )
            )

        # Movement
        if world_slice.current_room is not None:

            actions.append(
                PlannedAction(
                    action="move",
                    target=world_slice.current_room,
                )
            )

        return actions