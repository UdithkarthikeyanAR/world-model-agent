"""

Splits a raw environment observation into normalized text segments.


The returned segments are later processed by:
    classifier.py
"""

from __future__ import annotations

import re


class ObservationSegmenter:
    """
    Splits an observation into normalized text segments.

    Example
    -------
    Input:

        You are in the kitchen.
        A key is on the table.

        Exits: North, East.

    Output:

        [
            "You are in the kitchen.",
            "A key is on the table.",
            "Exits: North, East."
        ]
    """

    def segment(self, observation: str) -> list[str]:
        """
        Segment a raw observation.

        Parameters
        ----------
        observation:
            Raw text from the environment.

        Returns
        -------
        list[str]
            Clean list of observation segments.
        """

        observation = observation.strip()

        if not observation:
            return []

        # Normalize whitespace
        observation = re.sub(r"\r\n?", "\n", observation)

        # Split by newline
        lines = observation.split("\n")

        segments = []

        for line in lines:
            line = line.strip()

            if not line:
                continue

            # Collapse repeated spaces
            line = re.sub(r"\s+", " ", line)

            segments.append(line)

        return segments