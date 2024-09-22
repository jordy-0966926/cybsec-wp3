from src.lib.models.database_entity import DatabaseEntry
from src.lib.util.database import db_cursor as connect_db


class Class(DatabaseEntry):
    def __init__(self):
        super().__init__()
        self.table_name = 'classes'
        self.ukey_name = 'id'

    def seed_classes(self):
        """Seed the classes table with the default classes."""
        if self.get_table_count() == 0:
            class_names = ["1A", "1B", "1C", "1D", "1E"]
            classes = []
            for name in class_names:
                class_schema = {
                    'name': str(name)
                }
                classes.append(class_schema)
            self.set_table_data(classes)
            self.insert_data_in_db()

    def get_class_by_name(self, class_name: str) -> int:
        """Get the class_id by name."""
        qry = f"SELECT id FROM {self.table_name} WHERE name IS ?"
        cursor = connect_db()
        cursor.execute(qry, (class_name,))
        data = cursor.fetchone()
        return dict(data)
