"""
decision/model_client.py

Local LLM client.
Works even when Ollama is unavailable.
"""

from __future__ import annotations

try:
    import ollama
except ImportError:
    ollama = None


class ModelClient:

    def choose_action(
        self,
        observation: str,
        candidate_actions: list[str],
    ) -> str:

        if not candidate_actions:
            return ""

        # No Ollama installed
        if ollama is None:
            return candidate_actions[0]

        prompt = f"""
You are an intelligent agent playing a text adventure.

Observation:

{observation}

Available actions:

{chr(10).join("- " + a for a in candidate_actions)}

Choose EXACTLY one action.
Return ONLY the action text.
"""

        try:

            response = ollama.chat(
                model="qwen2.5:3b",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a decision-making AI.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )

            answer = response["message"]["content"].strip()

            for action in candidate_actions:

                if action.lower() == answer.lower():
                    return action

                if action.lower() in answer.lower():
                    return action

        except Exception:
            pass

        return candidate_actions[0]