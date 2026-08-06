"""
query/derived_views.py

Computes useful derived information from a WorldSlice.

This module never modifies the world.
It only derives information that helps the planner
make decisions quickly.
"""

from __future__ import annotations

from contracts.schema import Entity, Relation
from query.slice_builder import WorldSlice


class DerivedViews:
    """
    Produces useful computed views from a WorldSlice.
    """

    def reachable_rooms(self, world_slice: WorldSlice) -> list[int]:
        """
        Return IDs of rooms connected to the current room.
        """

        if world_slice.current_room is None:
            return []

        room_id = world_slice.current_room.id

        reachable = []

        for relation in world_slice.nearby_relations:
            if relation.source_id == room_id:
                reachable.append(relation.target_id)

        return reachable

    def interactable_entities(
        self,
        world_slice: WorldSlice,
    ) -> list[Entity]:
        """
        Return entities the agent can currently interact with.
        """

        return world_slice.visible_entities

    def usable_inventory(
        self,
        world_slice: WorldSlice,
    ) -> list[Entity]:
        """
        Return inventory items that may be used.
        """

        return world_slice.inventory

    def available_relations(
        self,
        world_slice: WorldSlice,
    ) -> list[Relation]:
        """
        Return relations available in the current slice.
        """

        return world_slice.nearby_relations