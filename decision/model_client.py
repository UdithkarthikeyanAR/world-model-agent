"""
decision/model_client.py

Local LLM client using Ollama.
"""

from __future__ import annotations



import ollama


class ModelClient:
    """
    Uses a local Qwen model to choose one action from a list.
    """

    def choose_action(
        self,
        observation: str,
        candidate_actions: list[str],
    ) -> str:

        prompt = f"""
You are an intelligent agent playing a text adventure.

Observation:

{observation}

Available actions:

{chr(10).join("- " + a for a in candidate_actions)}

Rules:
- Choose ONLY ONE action from the list.
- Do NOT invent new actions.
- Return ONLY the exact action text.
"""

        response = ollama.chat(
            model="qwen2.5:3b",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a decision-making AI for a text world."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
        )

        answer = response["message"]["content"].strip()

        # Make sure we always return a valid action
        for action in candidate_actions:
            if action.lower() in answer.lower():
                return action

        # Safe fallback
        return candidate_actions[0]