from pathlib import Path
from db.db_gen import WP3DatabaseGenerator
import sqlite3


db_file = "db/sqlite.db"

my_path = Path(__file__).parent.resolve()
project_root = my_path.parent.parent.parent.parent.parent
db_path = project_root / "db" / "sqlite.db"


def db_cursor():
    """Connect to the SQLite database."""

    if not db_path.exists():
        raise FileNotFoundError(f"Database file {db_file} does not exist")

    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()
    cursor.row_factory = sqlite3.Row

    return cursor


def db_check():
    """Check if the database exists."""
    return db_path.exists()


def db_create():
    """Create the database."""
    my_path = Path(__file__).parent.resolve()
    project_root = my_path.parent
    # Deze slashes komen uit de "Path" module. Dit is een module die je kan gebruiken
    # om paden te maken. Dit is handig omdat je dan niet zelf hoeft te kijken of je
    # een / (mac) of een \ (windows) moet gebruiken.

    database_generator = WP3DatabaseGenerator(
        db_path, overwrite=True, initial_data=True
    )
    database_generator.generate_database()
