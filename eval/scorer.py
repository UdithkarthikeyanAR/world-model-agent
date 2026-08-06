"""
eval/scorer.py

Computes evaluation metrics for benchmark runs.
"""

from __future__ import annotations

from dataclasses import dataclass

from eval.benchmark import BenchmarkCase


@dataclass(slots=True)
class ScoreReport:
    """
    Summary of benchmark performance.
    """

    total_cases: int
    passed_cases: int
    failed_cases: int
    accuracy: float


class Scorer:
    """
    Computes benchmark statistics.
    """

    def score(
        self,
        cases: list[BenchmarkCase],
    ) -> ScoreReport:
        """
        Calculate benchmark metrics.
        """

        total = len(cases)

        passed = sum(
            case.expected_action == case.predicted_action
            for case in cases
        )

        failed = total - passed

        accuracy = (
            (passed / total) * 100
            if total > 0
            else 0.0
        )

        return ScoreReport(
            total_cases=total,
            passed_cases=passed,
            failed_cases=failed,
            accuracy=accuracy,
        )