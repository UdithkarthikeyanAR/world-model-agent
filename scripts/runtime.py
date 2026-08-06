"""
scripts/runtime.py

Runtime pipeline for the Perception layer.

This module orchestrates the parser pipeline from a raw observation
to validated ParsedObservation objects.

Responsibilities
----------------
- Run the parser pipeline
- Return validated parser output
- Keep parser components loosely coupled

This module NEVER:
- modifies the database
- updates the world model
- assigns entity IDs
- performs planning
"""

from __future__ import annotations

from parser.segmenter import ObservationSegmenter
from parser.classifier import ObservationClassifier
from parser.extractor import ObservationExtractor
from parser.resolver import ObservationResolver
from parser.validator import ObservationValidator
from parser.models import ParsedObservation


class ParserRuntime:
    """
    Runs the complete perception pipeline.
    """

    def __init__(self) -> None:
        self.segmenter = ObservationSegmenter()
        self.classifier = ObservationClassifier()
        self.extractor = ObservationExtractor()
        self.resolver = ObservationResolver()
        self.validator = ObservationValidator()

    def process(self, observation: str) -> list[ParsedObservation]:
        """
        Process a raw observation through the parser pipeline.

        Parameters
        ----------
        observation : str
            Raw observation from the environment.

        Returns
        -------
        list[ParsedObservation]
            Valid parser outputs.
        """

        results: list[ParsedObservation] = []

        segments = self.segmenter.segment(observation)

        for segment in segments:

            segment_type = self.classifier.classify(segment)

            parsed = self.extractor.extract(segment, segment_type)

            parsed = self.resolver.resolve(parsed)

            is_valid, errors = self.validator.validate(parsed)

            if is_valid:
                results.append(parsed)
            else:
                print(f"[Validation Failed] {segment}")
                for error in errors:
                    print(f"  - {error}")

        return results


def main() -> None:
    """
    Simple runtime example.
    """

    runtime = ParserRuntime()

    observation = """
    You are in the kitchen.
    A silver key is on the wooden table.
    The door is locked.
    """

    parsed_observations = runtime.process(observation)

    for parsed in parsed_observations:
        print(parsed)


if __name__ == "__main__":
    main()