import sqlite3
from pathlib import Path

# Adapted from https://github.com/Rac-Software-Development/wp2-2023-starter/blob/main/lib/database/database_generator.py
# Original code written by markotting


class WP3DatabaseGenerator:
    def __init__(self, database_file, overwrite=False, initial_data=False):
        self.database_file = Path(database_file)
        self.create_initial_data = initial_data
        self.database_overwrite = overwrite
        self.test_file_location()
        self.conn = sqlite3.connect(self.database_file)

    def generate_database(self):
        self.create_table_students()
        self.create_table_teachers()
        self.create_table_classes()
        self.create_table_teams()
        self.create_table_statements()
        self.create_table_answers()

    def create_table_students(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            student_num TEXT NOT NULL,
            mbti TEXT,
            class_id INT,
            team_id INT,
            FOREIGN KEY (class_id) REFERENCES classes(id),
            FOREIGN KEY (team_id) REFERENCES teams(id)
        );
        """
        self.__execute_transaction_statement(create_statement)
        print("[SUCCESS] Students table created")

    def create_table_teachers(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS teachers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username text NOT NULL,
            password text NOT NULL,
            admin BOOLEAN NOT NULL DEFAULT 0
        );
        """
        self.__execute_transaction_statement(create_statement)
        print("[SUCCESS] Students teachers created")

    def create_table_classes(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS classes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
        """
        self.__execute_transaction_statement(create_statement)
        print("[SUCCESS] Classes table created")

    def create_table_teams(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        );
        """
        self.__execute_transaction_statement(create_statement)
        print("[SUCCESS] Teams table created")

    def create_table_statements(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS statements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            statement TEXT NOT NULL,
            type TEXT NOT NULL,
            prompt_id INT NOT NULL
        );
        """
        self.__execute_transaction_statement(create_statement)
        print("[SUCCESS] Statements table created")

    def create_table_answers(self):
        create_statement = """
        CREATE TABLE IF NOT EXISTS answers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            statement_id INTEGER NOT NULL,
            prompt_id INTEGER NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id),
            FOREIGN KEY (statement_id) REFERENCES statements(id)
        );
        """
        self.__execute_transaction_statement(create_statement)
        print("[SUCCESS] Answers table created")

    # Transacties zijn duur, dat wil zeggen, ze kosten veel tijd en CPU kracht. Als je veel insert doet
    # bundel je ze in één transactie, of je gebruikt de SQLite executemany methode.

    def __execute_transaction_statement(self, create_statement, parameters=()):
        c = self.conn.cursor()
        c.execute(create_statement, parameters)
        self.conn.commit()

    def test_file_location(self):
        if not self.database_file.parent.exists():
            raise ValueError(
                f"""Database file location {
                    self.database_file.parent} does not exist"""
            )
        if self.database_file.exists():
            if not self.database_overwrite:
                raise ValueError(
                    f"""Database file {
                        self.database_file} already exists, set overwrite=True to overwrite"""
                )
            else:
                # Unlink verwijdert een bestand
                self.database_file.unlink()
                print("[SUCCESS] Database already exists, deleted")
        if not self.database_file.exists():
            try:
                self.database_file.touch()
                print("[SUCCESS] New database setup")
            except Exception as e:
                raise ValueError(
                    f"""Could not create database file {
                        self.database_file} due to error {e}"""
                )


if __name__ == "__main__":
    my_path = Path(__file__).parent.resolve()
    project_root = my_path.parent
    # Deze slashes komen uit de "Path" module. Dit is een module die je kan gebruiken
    # om paden te maken. Dit is handig omdat je dan niet zelf hoeft te kijken of je
    # een / (mac) of een \ (windows) moet gebruiken.
    database_path = project_root / "db" / "sqlite.db"

    database_generator = WP3DatabaseGenerator(
        database_path, overwrite=True, initial_data=True
    )
    database_generator.generate_database()
