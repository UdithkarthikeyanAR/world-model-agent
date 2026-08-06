"""
decision/rules.py

Applies deterministic rules to the planner's candidate actions.

If a rule confidently selects an action,
the language model is never called.
"""

from __future__ import annotations

from decision.planner import PlannedAction


class RuleEngine:
    """
    Evaluates planned actions using deterministic rules.
    """

    def select_action(
        self,
        actions: list[PlannedAction],
    ) -> PlannedAction | None:
        """
        Return the first action that satisfies a rule.

        Returns None if no deterministic rule applies.
        """

        if not actions:
            return None

        # Rule 1:
        # Prefer interaction over inspection.
        for action in actions:
            if action.action == "interact":
                return action

        # Rule 2:
        # Use inventory items if available.
        for action in actions:
            if action.action == "use":
                return action

        # Rule 3:
        # Otherwise inspect the environment.
        for action in actions:
            if action.action == "inspect":
                return action

        # Rule 4:
        # Finally, move.
        for action in actions:
            if action.action == "move":
                return action

        return None