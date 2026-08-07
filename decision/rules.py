"""
decision/rules.py

Deterministic symbolic reasoning engine.
"""

from __future__ import annotations

from decision.planner import PlannedAction


class RuleEngine:

    def __init__(self) -> None:

        self._scores = {
            "take": 100,
            "unlock": 95,
            "open": 80,
            "drop": 60,
            "move": 70,
        }

    # ---------------------------------------------------------

    def score_action(
        self,
        action: PlannedAction,
    ) -> int:
        """
        Score an executable action.

        Example:

            take silver key
                ↓
            take
        """

        if not action.action:
            return 0

        verb = action.action.split()[0].lower()

        return self._scores.get(verb, 0)

    # ---------------------------------------------------------

    def rank_actions(
        self,
        actions: list[PlannedAction],
    ) -> list[tuple[PlannedAction, int]]:

        ranked = [
            (action, self.score_action(action))
            for action in actions
        ]

        ranked.sort(
            key=lambda x: x[1],
            reverse=True,
        )

        return ranked

    # ---------------------------------------------------------

    def confidence(
        self,
        ranked: list[tuple[PlannedAction, int]],
    ) -> float:

        if not ranked:
            return 0.0

        if len(ranked) == 1:
            return 1.0

        best = ranked[0][1]
        second = ranked[1][1]

        if best == 0:
            return 0.0

        return (best - second) / best

    # ---------------------------------------------------------

    def select_action(
        self,
        actions: list[PlannedAction],
    ) -> PlannedAction | None:

        ranked = self.rank_actions(actions)

        if not ranked:
            return None

        return ranked[0][0]