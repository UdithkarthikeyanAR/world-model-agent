"""
updater/revision_log.py

Revision logging for the World Model.

Responsibilities:
- Record successful updates
- Maintain revision history
- Provide access to previous revisions

This module should NOT:
- Execute SQL
- Apply updates
- Resolve conflicts
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from contracts.schema import UpdateEvent


# -------------------------------------------------------
# Revision Entry
# -------------------------------------------------------

@dataclass(slots=True)
class RevisionEntry:
    """
    Represents a single revision in the world model.
    """

    timestamp: datetime
    entity_id: int
    field: str
    old_value: Any
    new_value: Any


# -------------------------------------------------------
# Revision Logger
# -------------------------------------------------------

class RevisionLogger:
    """
    Stores revision history for applied updates.
    """

    def __init__(self) -> None:
        """
        Initialize an empty revision history.
        """

        self._history: list[RevisionEntry] = []

    # -------------------------------------------------------
    # Logging
    # -------------------------------------------------------

    def log(self, update: UpdateEvent) -> None:
        """
        Record a successfully applied update.
        """

        entry = RevisionEntry(
            timestamp=datetime.now(),
            entity_id=update.entity_id,
            field=update.field,
            old_value=update.old_value,
            new_value=update.new_value,
        )

        self._history.append(entry)

    # -------------------------------------------------------
    # Queries
    # -------------------------------------------------------

    def history(self) -> list[RevisionEntry]:
        """
        Return the complete revision history.
        """

        return list(self._history)

    def latest(self) -> RevisionEntry | None:
        """
        Return the most recent revision.
        """

        if not self._history:
            return None

        return self._history[-1]

    def count(self) -> int:
        """
        Return the number of stored revisions.
        """

        return len(self._history)

    # -------------------------------------------------------
    # Maintenance
    # -------------------------------------------------------

    def clear(self) -> None:
        """
        Remove all revision history.
        """

        self._history.clear()