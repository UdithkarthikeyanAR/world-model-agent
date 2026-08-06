"""
worldmodel/graph.py

Graph abstraction layer for the World Model.

This module provides graph-based operations on top of the
WorldStore without exposing SQLite.

Responsibilities:
- Graph traversal
- Neighbor lookup
- Location lookup
- Container lookup

This module should NOT:
- Execute SQL directly
- Modify parser logic
- Perform decision making
"""
from __future__ import annotations
from contracts.schema import Entity, Relation, RelationType
from worldmodel.store import WorldStore


class WorldGraph:
    """
    High-level graph interface for querying the world model.
    """

    def __init__(self, store: WorldStore):
        """
        Initialize the graph with a WorldStore instance.
        """
        self.store = store

    # -------------------------------------------------------
    # Entity Operations
    # -------------------------------------------------------

    def entity_exists(self, entity_id: int) -> bool:
        """
        Check whether an entity exists in the world.
        """
        return self.store.entity_exists(entity_id)

    # -------------------------------------------------------
    # Graph Operations
    # -------------------------------------------------------

    def get_neighbors(self, entity_id: int) -> list[int]:
        """
        Return IDs of all entities directly connected to the given entity.

        Example:

        Player --in--> Kitchen

        returns

        [Kitchen]
        """

        relations = self.store.get_relations(entity_id)

        return [
            relation.target_id
            for relation in relations
        ]

    def get_relations(self, entity_id: int) -> list[Relation]:
        """
        Return all outgoing relations for an entity.
        """
        return self.store.get_relations(entity_id)

    def get_entity(self, entity_id: int) -> Entity | None:
        """
        Retrieve an entity by ID.
        """
        return self.store.get_entity(entity_id)

    def list_entities(self) -> list[Entity]:
        """
        Return all entities in the world.
        """
        return self.store.list_entities()
    # -------------------------------------------------------
    # World Query Operations
    # -------------------------------------------------------

    def objects_in_room(self, room_id: int) -> list[Entity]:
        """
        Return every entity directly inside a room.
        """

        objects: list[Entity] = []

        relations = self.store.get_relations_to(room_id)

        for relation in relations:

            entity = self.store.get_entity(relation.source_id)

            if entity is not None:
                objects.append(entity)

        return objects


    def get_contents(self, container_id: int) -> list[Entity]:
        """
        Return every entity inside a container.
        """

        contents: list[Entity] = []

        relations = self.store.get_relations_to(container_id)

        for relation in relations:

            entity = self.store.get_entity(relation.source_id)

            if entity is not None:
                contents.append(entity)

        return contents


    def entity_location(self, entity_id: int) -> Entity | None:
        """
        Return the location/container of an entity.
        """

        relations = self.store.get_relations(entity_id)

        if not relations:
            return None

        location_id = relations[0].target_id

        return self.store.get_entity(location_id)


    def connected_entities(self, entity_id: int) -> list[Entity]:
        """
        Return all entities directly connected to an entity.
        """

        connected: list[Entity] = []

        relations = self.store.get_relations(entity_id)

        for relation in relations:

            entity = self.store.get_entity(relation.target_id)

            if entity is not None:
                connected.append(entity)

        return connected
    
    # -------------------------------------------------------
    # Graph Traversal
    # -------------------------------------------------------

    def path_exists(self, start_id: int, goal_id: int) -> bool:
        """
        Return True if a path exists between two entities.
        """

        return len(self.find_path(start_id, goal_id)) > 0


    def find_path(self, start_id: int, goal_id: int) -> list[int]:
        """
        Find a path between two entities using Breadth-First Search (BFS).

        Returns:
            List of entity IDs representing the path.
            Empty list if no path exists.
        """

        if start_id == goal_id:
            return [start_id]

        visited: set[int] = set()
        queue: list[tuple[int, list[int]]] = [(start_id, [start_id])]

        while queue:

            current, path = queue.pop(0)

            if current in visited:
                continue

            visited.add(current)

            neighbors = self.get_neighbors(current)

            for neighbor in neighbors:

                if neighbor == goal_id:
                    return path + [neighbor]

                if neighbor not in visited:
                    queue.append(
                        (
                            neighbor,
                            path + [neighbor],
                        )
                    )

        return []


    def reachable_entities(self, start_id: int) -> list[int]:
        """
        Return every entity reachable from a starting entity.
        """

        visited: set[int] = set()
        queue: list[int] = [start_id]

        while queue:

            current = queue.pop(0)

            if current in visited:
                continue

            visited.add(current)

            for neighbor in self.get_neighbors(current):

                if neighbor not in visited:
                    queue.append(neighbor)

        return list(visited)