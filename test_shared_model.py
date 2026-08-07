from shared.world_model import SharedWorldModel

world = SharedWorldModel()

print()

print("INITIAL")

print(world.summary())

print()

world.add_relation(

    "Laptop",

    "near",

    "Person",

)

print(world.export())