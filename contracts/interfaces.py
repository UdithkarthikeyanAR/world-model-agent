"""
contracts/interfaces.py

Canonical interfaces for the World Model Agent.

Every module in the project should communicate through these
interfaces instead of concrete implementations.

This file contains NO implementation logic.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Iterable, Optional

from contracts.schema import (
    Entity,
    Relation,
    Property,
    PlayerState,
    WorldState,
    UpdateEvent,
)


# ==========================================================
# Entity Repository
# ==========================================================

class IEntityRepository(ABC):
    """Interface for entity storage."""

    @abstractmethod
    def add_entity(self, entity: Entity) -> None:
        ...

    @abstractmethod
    def get_entity(self, entity_id: int) -> Optional[Entity]:
        ...

    @abstractmethod
    def get_entity_by_name(self, name: str) -> Optional[Entity]:
        ...

    @abstractmethod
    def update_entity(self, entity: Entity) -> None:
        ...

    @abstractmethod
    def delete_entity(self, entity_id: int) -> None:
        ...

    @abstractmethod
    def list_entities(self) -> list[Entity]:
        ...

    @abstractmethod
    def entity_exists(self, entity_id: int) -> bool:
        ...


# ==========================================================
# Relation Repository
# ==========================================================

class IRelationRepository(ABC):
    """Interface for relation storage."""

    @abstractmethod
    def add_relation(self, relation: Relation) -> None:
        ...

    @abstractmethod
    def remove_relation(self, relation: Relation) -> None:
        ...

    @abstractmethod
    def get_relations(self, entity_id: int) -> list[Relation]:
        ...

    @abstractmethod
    def relation_exists(self, relation: Relation) -> bool:
        ...


# ==========================================================
# Property Repository
# ==========================================================

class IPropertyRepository(ABC):
    """Interface for entity properties."""

    @abstractmethod
    def set_property(self, prop: Property) -> None:
        ...

    @abstractmethod
    def get_property(self, entity_id: int, key: str) -> Optional[Property]:
        ...

    @abstractmethod
    def remove_property(self, entity_id: int, key: str) -> None:
        ...

    @abstractmethod
    def get_properties(self, entity_id: int) -> list[Property]:
        ...


# ==========================================================
# Player Repository
# ==========================================================

class IPlayerRepository(ABC):
    """Interface for player state."""

    @abstractmethod
    def get_player_state(self) -> PlayerState:
        ...

    @abstractmethod
    def update_player_state(self, state: PlayerState) -> None:
        ...


# ==========================================================
# World Store
# ==========================================================

class IWorldStore(
    IEntityRepository,
    IRelationRepository,
    IPropertyRepository,
    IPlayerRepository,
    ABC,
):
    """
    High-level interface exposed to the rest of the system.
    """

    @abstractmethod
    def get_world_state(self) -> WorldState:
        ...

    @abstractmethod
    def get_visible_entities(self) -> list[Entity]:
        ...

    @abstractmethod
    def apply_updates(self, updates: Iterable[UpdateEvent]) -> None:
        ...

    @abstractmethod
    def clear_world(self) -> None:
        ...

    @abstractmethod
    def commit(self) -> None:
        ...

    @abstractmethod
    def rollback(self) -> None:
        ...


# ==========================================================
# Updater
# ==========================================================

class IUpdater(ABC):
    """Interface for state updates."""

    @abstractmethod
    def apply_updates(self, updates: Iterable[UpdateEvent]) -> None:
        ...


# ==========================================================
# Revision Logger
# ==========================================================

class IRevisionLogger(ABC):
    """Interface for revision history."""

    @abstractmethod
    def log_revision(self, description: str) -> None:
        ...

    @abstractmethod
    def get_history(self) -> list[Any]:
        ...