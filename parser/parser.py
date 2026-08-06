"""
parser/parser.py

High-level parser facade.

Coordinates all parser components and exposes a single parse()
method to the rest of the system.
"""

from __future__ import annotations

from parser.segmentar import ObservationSegmenter
from parser.classifier import ObservationClassifier
from parser.extractor import ObservationExtractor
from parser.resolver import ObservationResolver
from parser.validator import ObservationValidator
from parser.models import ParsedObservation


class Parser:
    """
    High-level parser interface.
    """

    def __init__(self) -> None:

        self.segmenter = ObservationSegmenter()
        self.classifier = ObservationClassifier()
        self.extractor = ObservationExtractor()
        self.resolver = ObservationResolver()
        self.validator = ObservationValidator()

    def parse(self, observation: str) -> ParsedObservation:
        """
        Parse a raw observation into a single ParsedObservation.
        """

        # Split observation into segments
        segments = self.segmenter.segment(observation)

        # Final merged observation
        merged = ParsedObservation()

        # Process every segment independently
        for segment in segments:

            segment_type = self.classifier.classify(segment)

            partial = self.extractor.extract(
                segment,
                segment_type,
            )

            merged.entities.extend(partial.entities)
            merged.relations.extend(partial.relations)
            merged.properties.extend(partial.properties)
            merged.metadata.update(partial.metadata)

        # Normalize parser output
        merged = self.resolver.resolve(merged)

        # Validate
        valid, errors = self.validator.validate(merged)

        if not valid:
            raise ValueError(
                "Parser validation failed:\n"
                + "\n".join(errors)
            )

        return merged