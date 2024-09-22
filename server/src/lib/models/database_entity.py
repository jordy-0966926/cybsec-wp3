import sqlite3
from typing import List
from server.src.lib.sql import Queries
from server.src.lib.util.database import db_cursor


class DatabaseEntry:
    def __init__(self):
        self.table_name = None
        self.ukey_name = None
        self.table_data = None

    def name_check(self):
        """Check if table_name and ukey_name are set."""
        return self.table_name is not None and self.ukey_name is not None

    def data_check(self):
        """Check if table_data is set."""
        return self.table_data is not None

    def set_table_data(self, table_data: List[dict]) -> None:
        """Set the table data."""
        self.table_data = table_data

    def insert_data_in_db(self) -> None:
        """Insert new data into the database table."""
        if not self.name_check() or not self.data_check():
            raise ValueError(
                "Table name, unique key name, and data must be set.")

        cursor = db_cursor()
        try:
            if len(self.table_data) == 1:
                qry = Queries.insert_in_table(
                    self.table_name, self.table_data[0].keys())
                values = tuple(self.table_data[0].values())
                cursor.execute(qry, values)
            else:
                qry = Queries.insert_in_table(
                    self.table_name, self.table_data[0].keys())
                cursor.executemany(qry, [tuple(row.values())
                                   for row in self.table_data])
            cursor.connection.commit()
        except sqlite3.Error as e:
            print(f"Error inserting into {self.table_name}: {e}")
            cursor.connection.rollback()
        finally:
            cursor.close()

    def get_table_count(self) -> int:
        """Get the number of entities in the database."""
        if not self.name_check():
            raise ValueError("Table name and unique key name must be set.")

        qry = Queries.get_count(self.table_name)
        cursor = db_cursor()
        cursor.execute(qry)
        count = cursor.fetchone()[0]
        return count

    def get_all_ids(self) -> List[int]:
        """Get the ids from all the entries in the table."""
        if not self.name_check():
            raise ValueError("Table name and unique key name must be set.")

        qry = f"SELECT {self.ukey_name} FROM {self.table_name}"
        cursor = db_cursor()
        cursor.execute(qry)
        ids = [row[0] for row in cursor.fetchall()]
        return ids

    @staticmethod
    def get_table_columns(table_name: str) -> List[str]:
        """Get the column names of a table."""
        qry = f"PRAGMA table_info({table_name})"
        cursor = db_cursor()
        cursor.execute(qry)
        columns = [row[1] for row in cursor.fetchall()]
        return columns

    def get_row_by_ids(self, id: int = None, ids: List[int] = None) -> List[dict]:
        """Get rows from the database by ID or list of IDs."""
        if id is None and ids is None:
            raise ValueError("Either 'id' or 'ids' must be provided.")

        rows = []
        cursor = db_cursor()

        try:
            if id is not None:
                qry = f"SELECT * FROM {self.table_name} WHERE {self.ukey_name} = ?"
                cursor.execute(qry, (str(id),))
                row = cursor.fetchone()
                if row:
                    rows.append(dict(row))

            if ids:
                # Create a placeholder for each id
                placeholders = ','.join(['?'] * len(ids))
                qry = f"SELECT * FROM {self.table_name} WHERE {self.ukey_name} IN ({placeholders})"
                cursor.execute(qry, tuple(str(id) for id in ids))
                rows.extend(dict(row) for row in cursor.fetchall())

        except sqlite3.Error as e:
            print(f"Error fetching rows: {e}")
        finally:
            cursor.close()

        return rows

    def get_rows(self, interval: int = None, limit: int = None) -> List[dict]:
        """Get all rows from the table."""
        cursor = db_cursor()
        try:
            if interval is not None and limit is not None:
                qry = f"SELECT * FROM {self.table_name} LIMIT ? OFFSET ?"

                cursor.execute(qry, (limit, interval))
                rows = [dict(row) for row in cursor.fetchall()]
                return rows
            else:
                row_ids = self.get_all_ids()
                return self.get_row_by_ids(ids=row_ids)
        except sqlite3.Error as e:
            print(f"Error fetching rows: {e}")
        finally:
            cursor.close()

    def update_row_by_id(self, single_id: int, new_data: dict) -> None:
        """Update a row in the database by id."""
        if self.name_check():
            # Construct the SET part of the SQL query with dict keys
            set_columns = ', '.join(
                [f"{column} = ?" for column in new_data.keys()])
            qry = f"UPDATE {self.table_name} SET {set_columns} WHERE id = ?"

            # Convert new_data values to a tuple for cursor.execute()
            values = tuple(new_data.values()) + (single_id,)

            cursor = db_cursor()
            try:
                cursor.execute(qry, values)
                cursor.connection.commit()
            except sqlite3.Error as e:
                print(f"Error updating {self.table_name}: {e}")
                cursor.connection.rollback()
        else:
            raise ValueError("Table name and unique key name must be set.")

    def delete_row_by_ids(self, single_id: int = None, ids: List[int] = []) -> None:
        """Delete rows in the database by id, by single id or by list of ids."""
        cursor = db_cursor()
        if single_id is None and not ids:
            return

        try:
            if single_id is not None:
                qry = f"DELETE FROM {self.table_name} WHERE id = ?"
                cursor.execute(qry, (str(single_id),))
                cursor.connection.commit()

            if ids:
                qry = f"DELETE FROM {self.table_name} WHERE id = ?"
                for id_value in ids:
                    cursor.execute(qry, (str(id_value),))
                cursor.connection.commit()

        except sqlite3.Error as e:
            print(f"Error deleting from {self.table_name}: {e}")
            if cursor.connection:
                cursor.connection.rollback()
        finally:
            if cursor.connection:
                cursor.connection.close()
