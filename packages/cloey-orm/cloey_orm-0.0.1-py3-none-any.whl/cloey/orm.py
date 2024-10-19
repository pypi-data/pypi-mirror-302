import os
from typing import Type, TypeVar, Dict, Any, List, Optional
from datetime import datetime

from cloey.connection import BaseDBConnection
from cloey.database import SQLiteConnection

# Constants
MIGRATIONS_DIR = './migrations'
LOG_FILE = './logs/sql_queries.log'

T = TypeVar('T', bound='BaseModel')

# Global connection manager
db_connection: BaseDBConnection = SQLiteConnection("default.db")  # Default to SQLite


class BaseModel:
    __tablename__: str

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    @classmethod
    def set_connection(cls, connection: BaseDBConnection):
        """Set the database connection."""
        global db_connection
        db_connection = connection
        db_connection.connect()

    @classmethod
    def _log_sql(cls, query: str, params: tuple):
        """Log the SQL query with parameters."""
        log_dir = os.path.dirname(LOG_FILE)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        with open(LOG_FILE, 'a') as log_file:
            log_file.write(f"{datetime.now()} - Executing SQL: {query} | Parameters: {params}\n")

    @classmethod
    def get_connection(cls) -> any:
        """Get the current database connection."""
        return db_connection.get_connection()

    @classmethod
    def create_table(cls):
        """Create the table in the database."""
        conn = cls.get_connection()
        columns = cls._get_columns()
        columns_sql = ", ".join(columns)
        sql = f"CREATE TABLE IF NOT EXISTS {cls.__tablename__} ({columns_sql})"
        cls._log_sql(sql, ())
        db_connection.execute_query(sql)

    @classmethod
    def _get_columns(cls) -> List[str]:
        """Get the SQL column definitions for the model."""
        columns = []
        for key, value in cls.__annotations__.items():
            column_type = "TEXT"  # Default type
            if value == int:
                column_type = "INTEGER"
            columns.append(f"{key} {column_type}")
        return columns

    @classmethod
    def get_current_schema(cls) -> Dict[str, str]:
        """Get the current schema of the table."""
        conn = cls.get_connection()
        cursor = conn.execute(f"PRAGMA table_info({cls.__tablename__})")
        return {row[1]: row[2] for row in cursor.fetchall()}

    @classmethod
    def generate_migration_script(cls, old_schema: Dict[str, str], new_schema: Dict[str, str]) -> str:
        """Generate a migration script to update the table schema."""
        alter_statements = []

        # Detect added columns
        for column in new_schema:
            if column not in old_schema:
                alter_statements.append(f"ALTER TABLE {cls.__tablename__} ADD COLUMN {column} {new_schema[column]}")

        # Detect removed columns
        for column in old_schema:
            if column not in new_schema:
                # SQLite does not support DROP COLUMN directly, so we create a new table.
                alter_statements.append(
                    f"-- WARNING: Column {column} was removed. You need to recreate the table to remove columns.")

        return "\n".join(alter_statements)

    @classmethod
    def create_migration_file(cls, sql_commands: str):
        """Create a migration file with SQL commands."""
        if not os.path.exists(MIGRATIONS_DIR):
            os.makedirs(MIGRATIONS_DIR)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{MIGRATIONS_DIR}/migration_{cls.__tablename__}_{timestamp}.sql"

        with open(filename, 'w') as f:
            f.write(sql_commands)
            print(f"Migration script saved: {filename}")

    @classmethod
    def generate_and_save_migration(cls):
        """Generate and save the migration script."""
        old_schema = cls.get_current_schema()
        new_schema = {column.split()[0]: column.split()[1] for column in cls._get_columns()}

        if old_schema == new_schema:
            print("No changes detected, no migration needed.")
            return

        migration_script = cls.generate_migration_script(old_schema, new_schema)
        if migration_script:
            cls.create_migration_file(migration_script)

    @classmethod
    def ensure_migrations_table(cls):
        """Ensure that the migrations table exists."""
        conn = cls.get_connection()
        conn.execute("""
            CREATE TABLE IF NOT EXISTS migrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                migration TEXT NOT NULL,
                applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

    @classmethod
    def get_applied_migrations(cls) -> List[str]:
        """Get a list of applied migrations from the database."""
        cls.ensure_migrations_table()  # Ensure the table exists
        conn = cls.get_connection()
        cursor = conn.execute("SELECT migration FROM migrations")
        return [row[0] for row in cursor.fetchall()]

    @classmethod
    def apply_pending_migrations(cls):
        """Apply any migrations that have not been applied yet."""
        cls.ensure_migrations_table()  # Ensure the table exists
        applied_migrations = cls.get_applied_migrations()
        conn = cls.get_connection()
        for migration_file in sorted(os.listdir(MIGRATIONS_DIR)):
            if migration_file not in applied_migrations:
                with open(os.path.join(MIGRATIONS_DIR, migration_file)) as f:
                    sql = f.read()
                    cls._log_sql(sql, ())  # Log the migration script
                    db_connection.execute_query(sql)
                cls.record_migration(migration_file)
                print(f"Applied migration: {migration_file}")

    @classmethod
    def record_migration(cls, migration_name: str):
        """Record the migration in the migrations table."""
        cls.ensure_migrations_table()  # Ensure the table exists
        conn = cls.get_connection()
        cls._log_sql("INSERT INTO migrations (migration) VALUES (?)", (migration_name,))
        db_connection.execute_query("INSERT INTO migrations (migration) VALUES (?)", (migration_name,))

    @classmethod
    def create(cls, **kwargs):
        """Insert a new record into the table."""
        conn = cls.get_connection()
        columns = ", ".join(kwargs.keys())
        placeholders = ", ".join("?" for _ in kwargs.values())
        values = tuple(kwargs.values())
        sql = f"INSERT INTO {cls.__tablename__} ({columns}) VALUES ({placeholders})"
        cls._log_sql(sql, values)  # Log the query
        db_connection.execute_query(sql, values)

    @classmethod
    def find(cls, **kwargs) -> Optional[T]:
        """Find a record by given criteria."""
        conn = cls.get_connection()
        condition = " AND ".join(f"{key}=?" for key in kwargs.keys())
        values = tuple(kwargs.values())
        sql = f"SELECT * FROM {cls.__tablename__} WHERE {condition}"
        cls._log_sql(sql, values)  # Log the query
        cursor = conn.execute(sql, values)
        row = cursor.fetchone()
        if row:
            return cls(**dict(zip([column[0] for column in cursor.description], row)))
        return None

    @classmethod
    def all(cls) -> List[T]:
        """Get all records from the table."""
        conn = cls.get_connection()
        sql = f"SELECT * FROM {cls.__tablename__}"
        cls._log_sql(sql, ())  # Log the query
        cursor = conn.execute(sql)
        rows = cursor.fetchall()
        return [cls(**dict(zip([column[0] for column in cursor.description], row))) for row in rows]

    @classmethod
    def update(cls, data: Dict[str, Any], **conditions):
        """Update records based on conditions."""
        conn = cls.get_connection()
        update_fields = ", ".join(f"{key}=?" for key in data.keys())
        condition = " AND ".join(f"{key}=?" for key in conditions.keys())
        values = tuple(data.values()) + tuple(conditions.values())
        sql = f"UPDATE {cls.__tablename__} SET {update_fields} WHERE {condition}"
        cls._log_sql(sql, values)  # Log the query
        db_connection.execute_query(sql, values)

    @classmethod
    def delete(cls, **conditions):
        """Delete records based on conditions."""
        conn = cls.get_connection()
        condition = " AND ".join(f"{key}=?" for key in conditions.keys())
        values = tuple(conditions.values())
        sql = f"DELETE FROM {cls.__tablename__} WHERE {condition}"
        cls._log_sql(sql, values)  # Log the query
        db_connection.execute_query(sql, values)
