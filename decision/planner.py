"""
decision/planner.py

Generates executable candidate actions from the current WorldSlice.

The planner NEVER chooses the best action.
It ONLY generates valid actions.
"""

from __future__ import annotations

from dataclasses import dataclass

from contracts.schema import EntityType
from query.slice_builder import WorldSlice


@dataclass(slots=True)
class PlannedAction:
    """
    Represents one executable action.
    """

    action: str


class Planner:
    """
    Generates executable candidate actions.
    """

    def plan(
        self,
        world_slice: WorldSlice,
    ) -> list[PlannedAction]:

        actions: list[PlannedAction] = []

        # -------------------------------------------------
        # Visible entities
        # -------------------------------------------------

        for entity in world_slice.visible_entities:

            name = entity.name.lower()

            # -----------------------------
            # Items
            # -----------------------------

            if entity.entity_type == EntityType.ITEM:

                actions.append(
                    PlannedAction(
                        action=f"take {name}"
                    )
                )

            # -----------------------------
            # Containers
            # -----------------------------

            elif entity.entity_type == EntityType.CONTAINER:

                actions.append(
                    PlannedAction(
                        action=f"open {name}"
                    )
                )

            # -----------------------------
            # Doors
            # -----------------------------

            elif entity.entity_type == EntityType.DOOR:

                actions.append(
                    PlannedAction(
                        action=f"unlock {name}"
                    )
                )

                actions.append(
                    PlannedAction(
                        action=f"open {name}"
                    )
                )

        # -------------------------------------------------
        # Inventory
        # -------------------------------------------------

        for item in world_slice.inventory:

            name = item.name.lower()

            actions.append(
                PlannedAction(
                    action=f"drop {name}"
                )
            )

        # -------------------------------------------------
        # Remove duplicates
        # -------------------------------------------------

        unique: dict[str, PlannedAction] = {}

        for action in actions:
            unique[action.action] = action

        return list(unique.values())