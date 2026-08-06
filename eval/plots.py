"""
eval/plots.py

Utility functions for presenting evaluation results.

This module prepares benchmark results for visualization.
Actual plotting libraries can be integrated later.
"""

from __future__ import annotations

from eval.scorer import ScoreReport


class PlotGenerator:
    """
    Generates simple visualization-ready summaries
    from benchmark results.
    """

    def summary(self, report: ScoreReport) -> dict[str, float]:
        """
        Convert ScoreReport into a visualization-friendly format.
        """

        return {
            "Total Cases": report.total_cases,
            "Passed Cases": report.passed_cases,
            "Failed Cases": report.failed_cases,
            "Accuracy (%)": round(report.accuracy, 2),
        }

    def print_summary(self, report: ScoreReport) -> None:
        """
        Print a simple evaluation summary.
        """

        print("========== Evaluation Summary ==========")
        print(f"Total Cases   : {report.total_cases}")
        print(f"Passed Cases  : {report.passed_cases}")
        print(f"Failed Cases  : {report.failed_cases}")
        print(f"Accuracy      : {report.accuracy:.2f}%")
        print("========================================")