from contracts.schema import (
    Entity,
    EntityType,
    Relation,
    RelationType,
    Property,
    PlayerState,
)

from worldmodel.store import WorldStore


def main():
    # Create a fresh test database
    store = WorldStore("test_world.db")

    print("=== Clearing Database ===")
    store.clear_world()

    # --------------------------------------------------
    # Test Entity CRUD
    # --------------------------------------------------
    print("\n=== Entity CRUD ===")

    room = Entity(
        id=1,
        name="Kitchen",
        entity_type=EntityType.ROOM,
    )

    apple = Entity(
        id=2,
        name="Apple",
        entity_type=EntityType.OBJECT,
    )

    store.add_entity(room)
    store.add_entity(apple)

    print(store.list_entities())

    # --------------------------------------------------
    # Test Relation CRUD
    # --------------------------------------------------
    print("\n=== Relation CRUD ===")

    relation = Relation(
        source_id=2,
        relation=RelationType.INSIDE,
        target_id=1,
    )

    store.add_relation(relation)

    print(store.get_relations(2))

    # --------------------------------------------------
    # Test Property CRUD
    # --------------------------------------------------
    print("\n=== Property CRUD ===")

    prop = Property(
        entity_id=1,
        key="state",
        value="clean",
    )

    store.set_property(prop)

    print(store.get_property(1, "state"))

    # --------------------------------------------------
    # Test Player State
    # --------------------------------------------------
    print("\n=== Player State ===")

    player = PlayerState(
        player_id=99,
        current_room=1,
        inventory=[],
    )

    store.update_player_state(player)

    print(store.get_player_state())

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------
    print("\n=== Summary ===")
    print(store.world_summary())

    store.close()


if __name__ == "__main__":
    main()