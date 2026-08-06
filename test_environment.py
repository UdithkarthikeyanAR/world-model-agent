from environment.engine import EnvironmentEngine

env = EnvironmentEngine()

print("=" * 50)
print("INITIAL")
print("=" * 50)
print(env.observe())

print("\n" + "=" * 50)
print("TAKE KEY")
print("=" * 50)

print("Success:", env.execute("take key"))
print(env.observe())
print("Inventory:", env.world.inventory)

print("\n" + "=" * 50)
print("UNLOCK DOOR")
print("=" * 50)

print("Success:", env.execute("unlock north door"))
print(env.observe())

print("\n" + "=" * 50)
print("MOVE SOUTH")
print("=" * 50)

print("Success:", env.execute("move south"))
print(env.observe())