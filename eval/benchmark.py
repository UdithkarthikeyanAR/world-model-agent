"""
eval/benchmark.py

Runs benchmark scenarios against the World Model Agent.
"""

from __future__ import annotations

from dataclasses import dataclass

from decision.planner import PlannedAction


@dataclass(slots=True)
class BenchmarkCase:
    """
    Represents a single benchmark scenario.
    """

    name: str
    expected_action: str
    predicted_action: str


class BenchmarkRunner:
    """
    Executes benchmark cases.
    """

    def run(
        self,
        cases: list[BenchmarkCase],
    ) -> list[BenchmarkCase]:
        """
        Placeholder benchmark runner.

        Returns benchmark cases unchanged.
        """

        return cases