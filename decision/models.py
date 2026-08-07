"""
decision/models.py

Shared data models used by the decision layer.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ScoredAction:
    """
    Represents a candidate action after symbolic reasoning.
    """

    action: str
    score: float
    confidence: float
    explanation: str = ""