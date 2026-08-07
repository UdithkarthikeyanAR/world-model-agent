"""
main.py

Entry point for the Hybrid Neuro-Symbolic World Model Agent.
"""

from agent.agent import HybridAgent


def main():

    agent = HybridAgent()

    try:

        agent.run(
            max_steps=25
        )

    except KeyboardInterrupt:

        print("\nStopped by user.")

    finally:

        agent.store.close()


if __name__ == "__main__":
    main()