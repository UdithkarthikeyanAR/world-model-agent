"""
query/slice_builder.py

Builds a lightweight view of the current world state for the
decision engine.

The SliceBuilder never modifies the world.
It only extracts the information required for reasoning.
"""

from __future__ import annotations

from dataclasses import dataclass

from contracts.schema import (
    Entity,
    Relation,
    Property,
    WorldState,
)

EntityLookup = dict[int, Entity]

@dataclass(slots=True)
class WorldSlice:
    """
    A reduced view of the world used by the planner.
    """

    current_room: Entity | None
    visible_entities: list[Entity]
    inventory: list[Entity]
    nearby_relations: list[Relation]
    properties: list[Property]


class SliceBuilder:
    """
    Extracts a relevant subset of the WorldState.
    """

    def build_slice(self, world: WorldState) -> WorldSlice:
        """
        Build a reasoning slice from the complete world.
        """

        current_room = self._get_current_room(world)
        inventory_entities = self._get_inventory(world)
        visible_entities = self._get_visible_entities(world, current_room)
        room_relations = self._get_room_relations(world, current_room)
        entity_properties = self._get_properties(world, visible_entities)

        return WorldSlice(
            current_room=current_room,
            visible_entities=visible_entities,
            inventory=inventory_entities,
            nearby_relations=room_relations,
            properties=entity_properties,
)

    # ---------------------------------------------------------
    # Helper methods
    # ---------------------------------------------------------

    def _find_entity(
        self,
        world: WorldState,
        entity_id: int,
    ) -> Entity | None:
        """
        Find an entity by ID.
        """

        for entity in world.entities:
            if entity.id == entity_id:
                return entity

        return None

    def _get_current_room(
        self,
        world: WorldState,
    ) -> Entity | None:
        """
        Return the player's current room.
        """

        if world.player is None:
            return None

        return self._find_entity(world, world.player.current_room)

    def _get_inventory(
        self,
        world: WorldState,
    ) -> list[Entity]:
        """
        Return inventory entities.
        """

        if world.player is None:
            return []

        inventory = []

        for entity_id in world.player.inventory:
            entity = self._find_entity(world, entity_id)
            if entity:
                inventory.append(entity)

        return inventory

    def _get_visible_entities(
        self,
        world: WorldState,
        room: Entity | None,
    ) -> list[Entity]:
        """
        Return entities located inside the current room.
        """

        if room is None:
            return []

        visible = []

        for relation in world.relations:
            if relation.target_id == room.id:
                entity = self._find_entity(world, relation.source_id)
                if entity:
                    visible.append(entity)

        return visible

    def _get_room_relations(
        self,
        world: WorldState,
        room: Entity | None,
    ) -> list[Relation]:
        """
        Return relations involving the current room.
        """

        if room is None:
            return []

        return [
            relation
            for relation in world.relations
            if relation.source_id == room.id
            or relation.target_id == room.id
        ]

    def _get_properties(
        self,
        world: WorldState,
        entities: list[Entity],
    ) -> list[Property]:
        """
        Return properties belonging to visible entities.
        """

        entity_ids = {entity.id for entity in entities}

        return [
            prop
            for prop in world.properties
            if prop.entity_id in entity_ids
        ]