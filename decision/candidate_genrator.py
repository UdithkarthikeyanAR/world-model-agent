"""
decision/candidate_generator.py

Generates all possible actions from the current world state.

This module does NOT perform reasoning.

It only enumerates legal actions.
"""

from __future__ import annotations

from query.query_engine import QueryEngine

from contracts.schema import EntityType


class CandidateGenerator:

    def __init__(self, query: QueryEngine):

        self.query = query

    # ---------------------------------------------------------

    def generate(self) -> list[str]:

        actions: list[str] = []

        # ------------------------------------
        # Always available
        # ------------------------------------

        actions.append("look")

        actions.append("inventory")

        # ------------------------------------
        # Movement
        # ------------------------------------

        room = self.query.current_room()

        if room is not None:

            exits = self.query.outgoing_relations(
                room.id
            )

            for relation in exits:

                actions.append(
                    f"move {relation.relation.value}"
                )

        # ------------------------------------
        # Visible Items
        # ------------------------------------

        for item in self.query.visible_items():

            actions.append(
                f"take {item.name.lower()}"
            )

            actions.append(
                f"examine {item.name.lower()}"
            )

        # ------------------------------------
        # Containers
        # ------------------------------------

        for container in self.query.containers():

            prop = self.query.property(
                container.id,
                "opened",
            )

            if prop is None:

                actions.append(
                    f"open {container.name.lower()}"
                )

            else:

                if str(prop.value).lower() == "false":

                    actions.append(
                        f"open {container.name.lower()}"
                    )

                else:

                    actions.append(
                        f"close {container.name.lower()}"
                    )

        # ------------------------------------
        # Doors
        # ------------------------------------

        for door in self.query.doors():

            locked = self.query.property(
                door.id,
                "locked",
            )

            if locked is not None:

                if str(locked.value).lower() == "true":

                    actions.append(
                        f"unlock {door.name.lower()}"
                    )

                else:

                    actions.append(
                        f"open {door.name.lower()}"
                    )

        return sorted(set(actions))