"""
updater/precedence.py

Conflict resolution for World Model updates.

Responsibilities:
- Compare competing updates
- Decide which update wins
- Keep conflict resolution separate from the updater
"""

from __future__ import annotations

from contracts.schema import UpdateEvent


class PrecedenceResolver:
    """
    Resolves conflicts between competing UpdateEvents.
    """

    def __init__(self) -> None:
        pass

    # -------------------------------------------------------
    # Public API
    # -------------------------------------------------------

    def choose(
        self,
        first: UpdateEvent,
        second: UpdateEvent,
    ) -> UpdateEvent:
        """
        Return the update with higher precedence.

        Current rule:
        - Newer timestamp wins.
        - If equal, keep the first update.
        """

        if second.timestamp > first.timestamp:
            return second

        return first

    def choose_many(
        self,
        updates: list[UpdateEvent],
    ) -> list[UpdateEvent]:
        """
        Resolve conflicts among multiple updates.

        Returns one winning update for each
        (entity_id, field) pair.
        """

        winners: dict[tuple[int, str], UpdateEvent] = {}

        for update in updates:

            key = (
                update.entity_id,
                update.field,
            )

            if key not in winners:
                winners[key] = update

            else:
                winners[key] = self.choose(
                    winners[key],
                    update,
                )

        return list(winners.values())