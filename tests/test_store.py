from pathlib import Path

from worldmodel.store import WorldStore

from contracts.schema import (
    Entity,
    EntityType,
    Relation,
    RelationType,
)

# -------------------------
# Fresh Database
# -------------------------

db = Path("test_world.db")

if db.exists():
    db.unlink()

store = WorldStore("test_world.db")

print("========== RELATION CRUD TEST ==========\n")

# -------------------------
# Create Entities
# -------------------------

kitchen = Entity(
    id=1,
    name="Kitchen",
    entity_type=EntityType.ROOM,
)

table = Entity(
    id=2,
    name="Table",
    entity_type=EntityType.SURFACE,
)

key = Entity(
    id=3,
    name="Silver Key",
    entity_type=EntityType.ITEM,
)

store.add_entity(kitchen)
store.add_entity(table)
store.add_entity(key)

print("✅ Entities created.\n")

# -------------------------
# Create Relation
# -------------------------

relation = Relation(
    source_id=3,
    relation=RelationType.ON,
    target_id=2,
)

store.add_relation(relation)

print("✅ Relation added.\n")

# -------------------------
# Get Relations FROM Key
# -------------------------

print("Relations FROM Silver Key:")

for r in store.get_relations(3):
    print(r)

# -------------------------
# Get Relations TO Table
# -------------------------

print("\nRelations TO Table:")

for r in store.get_relations_to(2):
    print(r)

store.close()