from environment.engine import EnvironmentEngine

env = EnvironmentEngine()

print("=" * 50)
print("WORLD MODEL AGENT - ENVIRONMENT TEST")
print("=" * 50)

while True:

    print("\n" + "=" * 50)
    print(env.observe())

    action = input("\nAction (or 'quit'): ").strip()

    if action.lower() == "quit":
        break

    success = env.execute(action)

    print(f"\nSuccess: {success}")