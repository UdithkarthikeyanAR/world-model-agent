"""
decision/selector.py

Hybrid action selector.

Pipeline

Planner
    ↓
Rule Engine
    ↓
Confidence
    ├── High confidence → Symbolic action
    └── Low confidence  → Local Qwen (Ollama)
"""

from __future__ import annotations

from decision.model_client import ModelClient
from decision.planner import PlannedAction
from decision.rules import RuleEngine


class ActionSelector:
    """
    Hybrid Neuro-Symbolic action selector.
    """

    def __init__(
        self,
        confidence_threshold: float = 0.25,
    ) -> None:

        self.rules = RuleEngine()
        self.model = ModelClient()

        self.confidence_threshold = confidence_threshold

    # ---------------------------------------------------------

    def select(
        self,
        observation: str,
        actions: list[PlannedAction],
    ) -> PlannedAction | None:
        """
        Select the best action.

        High confidence:
            Symbolic reasoning.

        Low confidence:
            Ask local Qwen.
        """

        if not actions:
            return None

        ranked = self.rules.rank_actions(actions)

        confidence = self.rules.confidence(ranked)

        # ------------------------------------------
        # Symbolic reasoning is confident
        # ------------------------------------------

        if confidence >= self.confidence_threshold:
            return ranked[0][0]

        # ------------------------------------------
        # Low confidence
        # Ask the local SLM
        # ------------------------------------------

        candidate_strings = [
            action.action
            for action, _ in ranked[:5]
        ]

        chosen = self.model.choose_action(
            observation,
            candidate_strings,
        )

        for action, _ in ranked:

            if action.action == chosen:
                return action

        # Safe fallback
        return ranked[0][0]