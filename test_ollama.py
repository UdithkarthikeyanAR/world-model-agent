from decision.model_client import ModelClient

client = ModelClient()

observation = """
You are in the kitchen.
A silver key is on the wooden table.
The refrigerator is closed.
The north door is locked.
"""

actions = [
    "Take Silver Key",
    "Open Refrigerator",
    "Move South",
]

result = client.choose_action(
    observation,
    actions,
)

print("\nChosen Action:")
print(result)