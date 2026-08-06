"""
decision/selector.py

Coordinates the decision process.

The selector first tries deterministic rules.
If no rule applies, it falls back to the language model.
"""

from __future__ import annotations

from decision.model_client import ModelClient
from decision.planner import PlannedAction
from decision.rules import RuleEngine


class ActionSelector:
    """
    Coordinates rule-based and AI-based decision making.
    """

    def __init__(self) -> None:
        self.rule_engine = RuleEngine()
        self.model_client = ModelClient()

    def select_action(
        self,
        actions: list[PlannedAction],
    ) -> PlannedAction | None:
        """
        Select the best action.

        Priority:
        1. Rule Engine
        2. Language Model
        """

        rule_action = self.rule_engine.select_action(actions)

        if rule_action is not None:
            return rule_action

        return self.model_client.select_action(actions)