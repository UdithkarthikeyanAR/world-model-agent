"""
worldmodel/store.py

SQLite storage layer for the World Model.

Responsibilities:
- Database connection
- Table creation
- CRUD operations
- Transaction management

This module should NOT contain:
- Parser logic
- Decision logic
- Conflict resolution
"""

from contracts.schema import (
    Entity,
    EntityType,
    Relation,
    RelationType,
    Property,
    PlayerState,
)
import sqlite3
from pathlib import Path
from typing import Optional


class WorldStore:
    """
    Handles all interactions with the SQLite database.
    """

    def __init__(self, db_path: str = "world.db"):
        """
        Initialize the database connection and create tables.
        """

        self.db_path = Path(db_path)

        self.connection: Optional[sqlite3.Connection] = None
        self.cursor: Optional[sqlite3.Cursor] = None

        self.connect()
        self.create_tables()

    def connect(self) -> None:
        """
        Open a connection to the SQLite database.
        """

        self.connection = sqlite3.connect(self.db_path)

        # Allows accessing columns by name instead of index
        self.connection.row_factory = sqlite3.Row

        self.cursor = self.connection.cursor()

    def close(self) -> None:
        """
        Close the database connection.
        """

        if self.connection is not None:
            self.connection.close()

            self.connection = None
            self.cursor = None

    def commit(self) -> None:
        """
        Save all pending changes to the database.
        """

        if self.connection is not None:
            self.connection.commit()

    def rollback(self) -> None:
        """
        Undo all changes since the last commit.
        """

        if self.connection is not None:
            self.connection.rollback()

    def create_tables(self) -> None:
        """
        Create all required database tables if they do not already exist.
        """

        assert self.cursor is not None

        # --------------------------
        # Entities
        # --------------------------
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                entity_type TEXT NOT NULL
            )
        """)

        # --------------------------
        # Relations
        # --------------------------
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS relations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER NOT NULL,
                relation TEXT NOT NULL,
                target_id INTEGER NOT NULL,

                FOREIGN KEY(source_id) REFERENCES entities(id),
                FOREIGN KEY(target_id) REFERENCES entities(id)
            )
        """)

        # --------------------------
        # Properties
        # --------------------------
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS properties (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                entity_id INTEGER NOT NULL,
                key TEXT NOT NULL,
                value TEXT NOT NULL,

                FOREIGN KEY(entity_id) REFERENCES entities(id)
            )
        """)

        # --------------------------
        # Player State
        # --------------------------
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS player_state (
                player_id INTEGER PRIMARY KEY,
                current_room INTEGER,
                inventory_count INTEGER DEFAULT 0,

                FOREIGN KEY(player_id) REFERENCES entities(id),
                FOREIGN KEY(current_room) REFERENCES entities(id)
            )
        """)

        # --------------------------
        # Revision Log
        # --------------------------
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS revisions (
                revision_id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                description TEXT NOT NULL
            )
        """)

        self.connection.commit()
        # -------------------------------------------------------
        # Entity Operations
        # -------------------------------------------------------

    def add_entity(self, entity: Entity) -> None:
        """
        Insert a new entity into the world model.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            INSERT INTO entities (
                id,
                name,
                entity_type
            )
            VALUES (?, ?, ?)
            """,
            (
                entity.id,
                entity.name,
                entity.entity_type,
            ),
        )

        self.commit()


    def get_entity(self, entity_id: int) -> Optional[Entity]:
        """
        Retrieve an entity by its unique ID.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            SELECT
                id,
                name,
                entity_type
            FROM entities
            WHERE id = ?
            """,
            (entity_id,),
        )

        row = self.cursor.fetchone()

        if row is None:
            return None
        
        return Entity(
            id=row["id"],
            name=row["name"],
            entity_type=EntityType(row["entity_type"]),
        )


    def get_entity_by_name(self, name: str) -> Optional[Entity]:
        """
        Retrieve an entity by its name.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            SELECT
                id,
                name,
                entity_type
            FROM entities
            WHERE name = ?
            """,
            (name,),
        )

        row = self.cursor.fetchone()

        if row is None:
            return None

        return Entity(
            id=row["id"],
            name=row["name"],
            entity_type=EntityType(row["entity_type"]),
        )


    def update_entity(self, entity: Entity) -> None:
        """
        Update an existing entity.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            UPDATE entities
            SET
                name = ?,
                entity_type = ?
            WHERE id = ?
            """,
            (
                entity.name,
                entity.entity_type,
                entity.id,
            ),
        )

        self.commit()


    def delete_entity(self, entity_id: int) -> None:
        """
        Delete an entity from the database.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            DELETE FROM entities
            WHERE id = ?
            """,
            (entity_id,),
        )

        self.commit()


    def entity_exists(self, entity_id: int) -> bool:
        """
        Check whether an entity exists.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            SELECT 1
            FROM entities
            WHERE id = ?
            LIMIT 1
            """,
            (entity_id,),
        )

        return self.cursor.fetchone() is not None


    def list_entities(self) -> list[Entity]:
        """
        Return all entities.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            SELECT
                id,
                name,
                entity_type
            FROM entities
            ORDER BY id
            """
        )

        rows = self.cursor.fetchall()

        return [
            Entity(
                id=row["id"],
                name=row["name"],
                entity_type=EntityType(row["entity_type"]),
            )
            for row in rows
]


    def count_entities(self) -> int:
        """
        Return the total number of entities.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM entities
            """
        )

        return int(self.cursor.fetchone()[0])


    def clear_entities(self) -> None:
        """
        Remove every entity from the database.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            DELETE FROM entities
            """
        )

        self.commit()


    # -------------------------------------------------------
    # Relation Operations
    # -------------------------------------------------------

    def add_relation(self, relation: Relation) -> None:
        """
        Insert a new relationship between two entities.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            INSERT INTO relations (
                source_id,
                relation,
                target_id
            )
            VALUES (?, ?, ?)
            """,
            (
                relation.source_id,
                relation.relation.value,
                relation.target_id,
            ),
        )

        self.commit()


    def remove_relation(self, relation: Relation) -> None:
        """
        Remove a relationship.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            DELETE FROM relations
            WHERE
                source_id = ?
                AND relation = ?
                AND target_id = ?
            """,
            (
                relation.source_id,
                relation.relation.value,
                relation.target_id,
            ),
        )

        self.commit()


    def get_relations(self, entity_id: int) -> list[Relation]:
        """
        Return every relation where the entity is the source.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            SELECT
                source_id,
                relation,
                target_id
            FROM relations
            WHERE source_id = ?
            """,
            (entity_id,),
        )

        rows = self.cursor.fetchall()

        return [
            Relation(
                source_id=row["source_id"],
                relation=RelationType(row["relation"]),
                target_id=row["target_id"],
            )
            for row in rows
        ]

        
    def get_relations_to(self, target_id: int) -> list[Relation]:
        """
        Return every relation where the given entity is the target.

        This is useful for finding everything located inside a room
        or inside a container.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            SELECT
                source_id,
                relation,
                target_id
            FROM relations
            WHERE target_id = ?
            """,
            (target_id,),
        )

        rows = self.cursor.fetchall()

        return [
            Relation(
                source_id=row["source_id"],
                relation=RelationType(row["relation"]),
                target_id=row["target_id"],
            )
            for row in rows
        ]
    
    def relation_exists(self, relation: Relation) -> bool:
        """
        Check whether a relation already exists.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            SELECT 1
            FROM relations
            WHERE
                source_id = ?
                AND relation = ?
                AND target_id = ?
            LIMIT 1
            """,
            (
                relation.source_id,
                relation.relation.value,
                relation.target_id,
            ),
        )

        return self.cursor.fetchone() is not None


    def list_relations(self) -> list[Relation]:
        """
        Return every stored relation.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            SELECT
                source_id,
                relation,
                target_id
            FROM relations
            ORDER BY source_id
            """
        )

        rows = self.cursor.fetchall()

        return [
            Relation(
                source_id=row["source_id"],
                relation=RelationType(row["relation"]),
                target_id=row["target_id"],
            )
            for row in rows
        ]


    def clear_relations(self) -> None:
        """
        Remove all relations from the database.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            DELETE FROM relations
            """
        )

        self.commit()


    def count_relations(self) -> int:
        """
        Return the total number of relations.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM relations
            """
        )

        return int(self.cursor.fetchone()[0])
        
# -------------------------------------------------------
# Property Operations
# -------------------------------------------------------

    def set_property(self, prop: Property) -> None:
        """
        Insert or update a property for an entity.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            INSERT OR REPLACE INTO properties (
                entity_id,
                key,
                value
            )
            VALUES (?, ?, ?)
            """,
            (
                prop.entity_id,
                prop.key,
                str(prop.value),
            ),
        )

        self.commit()


    def get_property(
        self,
        entity_id: int,
        key: str,
    ) -> Optional[Property]:
        """
        Retrieve a property by key.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            SELECT
                entity_id,
                key,
                value
            FROM properties
            WHERE
                entity_id = ?
                AND key = ?
            """,
            (
                entity_id,
                key,
            ),
        )

        row = self.cursor.fetchone()

        if row is None:
            return None

        return Property(
            entity_id=row["entity_id"],
            key=row["key"],
            value=row["value"],
        )


    def get_properties(self, entity_id: int) -> list[Property]:
        """
        Return all properties attached to an entity.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            SELECT
                entity_id,
                key,
                value
            FROM properties
            WHERE entity_id = ?
            """,
            (entity_id,),
        )

        rows = self.cursor.fetchall()

        return [
            Property(
                entity_id=row["entity_id"],
                key=row["key"],
                value=row["value"],
            )
            for row in rows
        ]


    def remove_property(
        self,
        entity_id: int,
        key: str,
    ) -> None:
        """
        Remove a property from an entity.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            DELETE FROM properties
            WHERE
                entity_id = ?
                AND key = ?
            """,
            (
                entity_id,
                key,
            ),
        )

        self.commit()


    def clear_properties(self) -> None:
        """
        Remove every property.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            DELETE FROM properties
            """
        )

        self.commit()


    def count_properties(self) -> int:
        """
        Return the total number of properties.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            SELECT COUNT(*)
            FROM properties
            """
        )

        return int(self.cursor.fetchone()[0])
    
    # -------------------------------------------------------
    # Player State Operations
    # -------------------------------------------------------

    def get_player_state(self) -> Optional[PlayerState]:
        """
        Return the current player state.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            SELECT
                player_id,
                current_room,
                inventory_count
            FROM player_state
            LIMIT 1
            """
        )

        row = self.cursor.fetchone()

        if row is None:
            return None

        return PlayerState(
            player_id=row["player_id"],
            current_room=row["current_room"],
            inventory=[]
        )


    def update_player_state(self, state: PlayerState) -> None:
        """
        Insert or update the player state.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            INSERT OR REPLACE INTO player_state (
                player_id,
                current_room,
                inventory_count
            )
            VALUES (?, ?, ?)
            """,
            (
                state.player_id,
                state.current_room,
                len(state.inventory),
            ),
        )

        self.commit()


    def clear_player_state(self) -> None:
        """
        Remove player state.
        """

        assert self.cursor is not None

        self.cursor.execute(
            """
            DELETE FROM player_state
            """
        )

        self.commit()
    # -------------------------------------------------------
    # Utility Operations
    # -------------------------------------------------------

    def clear_world(self) -> None:
        """
        Remove all world data.
        """

        self.clear_relations()
        self.clear_properties()
        self.clear_entities()
        self.clear_player_state()


    def reset_database(self) -> None:
        """
        Reset the database to a clean state.
        """

        self.clear_world()


    def world_summary(self) -> dict[str, int]:
        """
        Return basic database statistics.
        """

        return {
            "entities": self.count_entities(),
            "relations": self.count_relations(),
            "properties": self.count_properties(),
        }


    def __enter__(self):
        """
        Support context manager usage.
        """
        return self


    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Automatically close the database.
        """

        self.close()