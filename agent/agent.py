"""
agent/agent.py

Main AI Agent.

Coordinates the complete Hybrid Neuro-Symbolic pipeline.

Pipeline

Environment
    ↓
Observation
    ↓
Parser
    ↓
WorldUpdater
    ↓
WorldStore
    ↓
SliceBuilder
    ↓
Planner
    ↓
RuleEngine
    ↓
ActionSelector
    ↓
Environment.execute()
"""

from __future__ import annotations

from environment.engine import EnvironmentEngine
from parser.parser import Parser

from worldmodel.store import WorldStore
from worldmodel.updater import WorldUpdater

from query.slice_builder import SliceBuilder

from decision.planner import Planner
from decision.selector import ActionSelector


class HybridAgent:
    """
    Hybrid Neuro-Symbolic Agent.
    """

    def __init__(
        self,
        db_path: str = "world.db",
    ) -> None:

        # -----------------------------
        # Environment
        # -----------------------------

        self.environment = EnvironmentEngine()

        # -----------------------------
        # Perception
        # -----------------------------

        self.parser = Parser()

        # -----------------------------
        # World Model
        # -----------------------------

        self.store = WorldStore(db_path)

        self.updater = WorldUpdater(
            self.store
        )

        # -----------------------------
        # Query
        # -----------------------------

        self.slice_builder = SliceBuilder()

        # -----------------------------
        # Decision
        # -----------------------------

        self.planner = Planner()

        self.selector = ActionSelector()

    # =====================================================

    def step(self) -> bool:

        # -----------------------------
        # Observe
        # -----------------------------

        observation = self.environment.observe()

        print("\n================================================")
        print("OBSERVATION")
        print("================================================")
        print(observation)

        # -----------------------------
        # Parse
        # -----------------------------

        parsed = self.parser.parse(
            observation
        )

        print("\n================================================")
        print("PARSED")
        print("================================================")

        print("Entities:")
        for entity in parsed.entities:
            print(
                f" - {entity.entity_type}: {entity.name}"
            )

        print("\nRelations:")
        for relation in parsed.relations:
            print(
                f" - {relation.source_name} "
                f"{relation.relation} "
                f"{relation.target_name}"
            )

        print("\nProperties:")
        for prop in parsed.properties:
            print(
                f" - {prop.entity_name}: "
                f"{prop.key}={prop.value}"
            )

        # -----------------------------
        # Update World Model
        # -----------------------------

        self.updater.update(parsed)

        # -----------------------------
        # Retrieve World
        # -----------------------------

        world = self.store.get_world_state()

        # -----------------------------
        # Build Slice
        # -----------------------------

        world_slice = self.slice_builder.build_slice(
            world
        )

        print("\n================================================")
        print("WORLD SLICE")
        print("================================================")

        print("Current Room:")

        if world_slice.current_room:
            print(world_slice.current_room.name)
        else:
            print("None")

        print("\nVisible Entities:")

        if world_slice.visible_entities:

            for entity in world_slice.visible_entities:

                print(
                    f" - {entity.name} "
                    f"({entity.entity_type})"
                )

        else:

            print("None")

        print("\nInventory:")

        if world_slice.inventory:

            for item in world_slice.inventory:

                print(
                    f" - {item.name}"
                )

        else:

            print("Empty")

        # -----------------------------
        # Planning
        # -----------------------------

        actions = self.planner.plan(
            world_slice
        )

        print("\n================================================")
        print("CANDIDATE ACTIONS")
        print("================================================")

        if actions:

            for action in actions:

                print(
                    " -",
                    action.action,
                )

        else:

            print("No candidate actions.")

            return False

        # -----------------------------
        # Selection
        # -----------------------------

        action = self.selector.select(
            observation,
            actions,
        )

        if action is None:

            print("\nNo action selected.")

            return False

        print("\n================================================")
        print("SELECTED ACTION")
        print("================================================")

        print(action.action)

        # -----------------------------
        # Execute
        # -----------------------------

        success = self.environment.execute(
            action.action
        )

        print("\nExecution Success:", success)

        return success

    # =====================================================

    def run(
        self,
        max_steps: int = 50,
    ) -> None:

        print("\nHybrid Neuro-Symbolic Agent Started")

        self.environment.reset()

        for step in range(max_steps):

            print(
                f"\n================ STEP {step+1} ================"
            )

            success = self.step()

            if not success:

                print("\nStopping agent.")

                break

        self.store.close()