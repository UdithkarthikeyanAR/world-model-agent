"""
updater/updater.py

Applies parser-generated updates to the World Model.

Responsibilities:
- Receive UpdateEvents
- Dispatch updates
- Coordinate WorldStore
- Coordinate RevisionLogger

This module should NOT:
- Execute SQL directly
- Parse language
- Perform planning
"""
from __future__ import annotations

from typing import Iterable

from contracts.schema import UpdateEvent

from worldmodel.store import WorldStore

from updater.revision_log import (
    RevisionLogger,
    RevisionEntry,
)

class WorldUpdater:
    """
    Applies updates to the world model.
    """

    def __init__(self, store: WorldStore):
        """
        Initialize the updater.
        """

        self.store = store
        self.logger = RevisionLogger()

    # -------------------------------------------------------
    # Public API
    # -------------------------------------------------------

    def apply_updates(
        self,
        updates: Iterable[UpdateEvent],
    ) -> None:
        """
        Apply multiple updates.
        """

        for update in updates:
            self.apply_update(update)

    def apply_update(
        self,
        update: UpdateEvent,
    ) -> None:
        """
        Apply a single validated update.
        """

        if not self.validate_update(update):
            raise ValueError("Invalid UpdateEvent.")

        if update.field == "entity":
            self.update_entity(update)

        elif update.field == "relation":
            self.update_relation(update)

        elif update.field == "property":
            self.update_property(update)

        elif update.field == "player":
            self.update_player(update)

        else:
            raise ValueError(
                f"Unknown update type: {update.field}"
            )

        # Log the successful update
        self.logger.log(update)

    def validate_update(
        self,
        update: UpdateEvent,
    ) -> bool:
        """
        Basic validation before applying an update.
        """

        if update.entity_id < 0:
            return False

        if not update.field:
            return False

        return True

    # -------------------------------------------------------
    # Update Handlers
    # -------------------------------------------------------

    def update_entity(
        self,
        update: UpdateEvent,
    ) -> None:
        """
        Update an existing entity.
        """

        entity = self.store.get_entity(update.entity_id)

        if entity is None:
            return

        entity.name = str(update.new_value)

        self.store.update_entity(entity)

    def update_relation(
        self,
        update: UpdateEvent,
    ) -> None:
        """
        Replace an entity's relation.
        """

        relation = update.new_value

        if relation is None:
            return

        self.store.add_relation(relation)

    def update_property(
        self,
        update: UpdateEvent,
    ) -> None:
        """
        Update an entity property.
        """

        prop = update.new_value

        if prop is None:
            return

        self.store.set_property(prop)

    def update_player(
        self,
        update: UpdateEvent,
    ) -> None:
        """
        Update player state.
        """

        player = update.new_value

        if player is None:
            return
        self.store.update_player_state(player)
            

    def clear(self) -> None:
        """
        Reset the entire world model.
        """

        self.store.clear_world()

    # -------------------------------------------------------
    # Revision History
    # -------------------------------------------------------

    def revision_history(self) -> list[RevisionEntry]:
        """
        Return the complete revision history.
        """

        return self.logger.history()

    def latest_revision(self) -> RevisionEntry | None:
        """
        Return the most recent revision.
        """

        return self.logger.latest()

    def clear_revision_history(self) -> None:
        """
        Remove all stored revisions.
        """

        self.logger.clear()
