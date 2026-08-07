"""
worldmodel/entity_registry.py

Maps parser entities to canonical World Model entities.

The parser only knows entity names.

The WorldStore requires persistent integer IDs.

This module bridges those two representations.
"""

from __future__ import annotations

from contracts.schema import (
    Entity,
    EntityType,
)

from worldmodel.store import WorldStore


class EntityRegistry:
    """
    Maintains a mapping between parser entities and
    canonical world entities stored in SQLite.
    """

    def __init__(self, store: WorldStore):

        self.store = store

        self._next_id = 1

    # ---------------------------------------------------------

    def resolve(
        self,
        name: str,
        entity_type: EntityType,
    ) -> Entity:
        """
        Return an existing entity or create a new one.
        """

        existing = self.store.get_entity_by_name(name)

        if existing is not None:
            return existing

        entity = Entity(
            id=self._allocate_id(),
            name=name,
            entity_type=entity_type,
        )

        self.store.add_entity(entity)

        return entity

    # ---------------------------------------------------------

    def exists(
        self,
        name: str,
    ) -> bool:

        return self.store.get_entity_by_name(name) is not None

    # ---------------------------------------------------------

    def get(
        self,
        name: str,
    ) -> Entity | None:

        return self.store.get_entity_by_name(name)

    # ---------------------------------------------------------

    def _allocate_id(self) -> int:
        """
        Allocate the next available entity ID.
        """

        entity_id = self._next_id

        self._next_id += 1

        return entity_id