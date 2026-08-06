"""
worldmodel/models.py

World Model helper models.

The canonical data models (Entity, Relation, Property,
PlayerState, WorldState) are defined in contracts/schema.py.

This module should only contain world-model-specific helper
models and should never redefine the shared schema.
"""

from dataclasses import dataclass
from datetime import datetime

from contracts.schema import (
    Entity,
    Relation,
    Property,
    PlayerState,
    WorldState,
)


@dataclass(slots=True)
class Revision:
    """
    Represents a change made to the world state.
    """

    revision_id: int
    timestamp: datetime
    description: str