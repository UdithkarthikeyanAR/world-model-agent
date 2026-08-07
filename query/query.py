"""
query/query_engine.py

Read-only interface to the Shared World Model.

All reasoning modules should query the world through this
class instead of accessing SQLite directly.
"""

from __future__ import annotations

from contracts.schema import (
    EntityType,
    RelationType,
)

from worldmodel.store import WorldStore


class QueryEngine:

    def __init__(self, store: WorldStore):

        self.store = store

    # ---------------------------------------------------------
    # Rooms
    # ---------------------------------------------------------

    def current_room(self):

        state = self.store.get_player_state()

        if state is None:
            return None

        return self.store.get_entity(
            state.current_room
        )

    # ---------------------------------------------------------
    # Inventory
    # ---------------------------------------------------------

    def inventory(self):

        state = self.store.get_player_state()

        if state is None:
            return []

        items = []

        for item_id in state.inventory:

            entity = self.store.get_entity(
                item_id
            )

            if entity is not None:
                items.append(entity)

        return items

    # ---------------------------------------------------------
    # Entities
    # ---------------------------------------------------------

    def all_entities(self):

        return self.store.list_entities()

    def entities_by_type(
        self,
        entity_type: EntityType,
    ):

        return [

            entity

            for entity in self.store.list_entities()

            if entity.entity_type == entity_type

        ]

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    def properties(self, entity_id: int):

        return self.store.get_properties(
            entity_id
        )

    def property(
        self,
        entity_id: int,
        key: str,
    ):

        return self.store.get_property(
            entity_id,
            key,
        )

    # ---------------------------------------------------------
    # Relations
    # ---------------------------------------------------------

    def outgoing_relations(
        self,
        entity_id: int,
    ):

        return self.store.get_relations(
            entity_id
        )

    def incoming_relations(
        self,
        entity_id: int,
    ):

        return self.store.get_relations_to(
            entity_id
        )

    # ---------------------------------------------------------
    # Visible Items
    # ---------------------------------------------------------

    def visible_items(self):

        room = self.current_room()

        if room is None:
            return []

        items = []

        relations = self.store.get_relations_to(
            room.id
        )

        for relation in relations:

            if relation.relation != RelationType.IN:
                continue

            entity = self.store.get_entity(
                relation.source_id
            )

            if entity is None:
                continue

            if entity.entity_type == EntityType.ITEM:

                items.append(entity)

        return items

    # ---------------------------------------------------------
    # Doors
    # ---------------------------------------------------------

    def doors(self):

        return self.entities_by_type(
            EntityType.DOOR
        )

    # ---------------------------------------------------------
    # Containers
    # ---------------------------------------------------------

    def containers(self):

        return self.entities_by_type(
            EntityType.CONTAINER
        )