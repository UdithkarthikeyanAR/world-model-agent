"""
decision/model_client.py

Interface to the local language model.

Currently this file contains a placeholder implementation.
It can later be connected to Ollama + Qwen 2.5 without
changing the rest of the project.
"""

from __future__ import annotations

from decision.planner import PlannedAction


class ModelClient:
    """
    Wrapper around the language model.
    """

    def select_action(
        self,
        actions: list[PlannedAction],
    ) -> PlannedAction | None:
        """
        Ask the language model to select the best action.

        Placeholder implementation.
        """

        if not actions:
            return None

        # TODO:
        # Replace this with an Ollama call.
        #
        # Example:
        #
        # prompt = ...
        # response = ollama.chat(...)
        # return parsed_action

        return actions[0]