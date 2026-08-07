"""
worldmodel/updater.py

Synchronizes parser output with the SQLite World Store.

Responsibilities
----------------
- Convert ParsedObservation into canonical schema objects.
- Create new entities when first discovered.
- Insert new relations.
- Update properties.
- Update player state when metadata is available.

This module performs NO reasoning.
"""


from __future__ import annotations

from contracts.schema import (
    Entity,
    Relation,
    Property,
    PlayerState,
    EntityType,
    RelationType,
)
from contracts.schema import RelationType
from parser.models import ParsedObservation

from worldmodel.store import WorldStore


class WorldUpdater:
    """
    Updates the persistent WorldStore using parser output.
    """

    def __init__(self, store: WorldStore):

        self.store = store

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------

    def update(
        self,
        observation: ParsedObservation,
    ) -> None:
        """
        Synchronize parser output with the WorldStore.
        """

        self._update_entities(observation)

        self._update_relations(observation)

        self._update_properties(observation)

        self._update_player_state(observation)

    # ---------------------------------------------------------
    # Entities
    # ---------------------------------------------------------

    def _update_entities(
        self,
        observation: ParsedObservation,
    ) -> None:

        next_id = self.store.count_entities() + 1

        for parsed in observation.entities:

            entity = self.store.get_entity_by_name(
                parsed.name
            )

            if entity is not None:
                continue

            entity = Entity(
                id=next_id,
                name=parsed.name,
                entity_type=parsed.entity_type,
            )

            self.store.add_entity(entity)

            next_id += 1

    # ---------------------------------------------------------
    # Relations
    # ---------------------------------------------------------

    def _update_relations(
        self,
        observation: ParsedObservation,
    ) -> None:

        for parsed in observation.relations:

            source = self.store.get_entity_by_name(
                parsed.source_name
            )

            target = self.store.get_entity_by_name(
                parsed.target_name
            )

            if source is None or target is None:
                continue

            relation = Relation(
                source_id=source.id,
                relation=parsed.relation,
                target_id=target.id,
            )

            if not self.store.relation_exists(
                relation
            ):
                self.store.add_relation(
                    relation
                )

    # ---------------------------------------------------------
    # Properties
    # ---------------------------------------------------------

    def _update_properties(
        self,
        observation: ParsedObservation,
    ) -> None:

        for parsed in observation.properties:

            entity = self.store.get_entity_by_name(
                parsed.entity_name
            )

            if entity is None:
                continue

            prop = Property(
                entity_id=entity.id,
                key=parsed.key,
                value=parsed.value,
            )

            self.store.set_property(prop)

    # ---------------------------------------------------------
    # Player State
    # ---------------------------------------------------------

    def _update_player_state(
        self,
        observation: ParsedObservation,
    ) -> None:

        metadata = observation.metadata

        player = self.store.get_entity_by_name(
            "Player"
        )

        if player is None:

            player = Entity(
                id=self.store.count_entities() + 1,
                name="Player",
                entity_type=EntityType.PLAYER,
            )

            self.store.add_entity(player)

        room_name = metadata.get(
            "current_room"
        )

        if room_name is None:
            return

        room = self.store.get_entity_by_name(
            room_name
        )

        if room is None:
            return

        inventory = []

        for item_name in metadata.get("inventory", []):

            entity = self.store.get_entity_by_name(item_name)

            if entity is not None:
                inventory.append(entity.id)

        state = PlayerState(
            player_id=player.id,
            current_room=room.id,
            inventory=inventory,
        )

        self.store.update_player_state(
            state
        )
        # -------------------------------------------------
        # TEMP: Place all discovered entities in current room
        # -------------------------------------------------

        for parsed in observation.entities:

            if parsed.entity_type == EntityType.ROOM:
                continue

            entity = self.store.get_entity_by_name(parsed.name)

            if entity is None:
                continue

            relation = Relation(
                source_id=entity.id,
                relation=RelationType.IN,
                target_id=room.id,
            )

            if not self.store.relation_exists(relation):
                self.store.add_relation(relation)