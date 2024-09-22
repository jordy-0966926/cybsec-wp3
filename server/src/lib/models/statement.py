from server.src.lib.models.database_entity import DatabaseEntry
from server.src.lib.util.database import db_cursor as connect_db
from server.src.lib.util.seed_data import actiontype_statements as json_file


class Statement(DatabaseEntry):
    def __init__(self):
        super().__init__()
        self.table_name = 'statements'
        self.ukey_name = 'id'

    def seed_statements(self):
        if self.get_table_count() == 0:
            statements = []
            for prompt in json_file:
                for statement in prompt['statement_choices']:
                    statement_schema = {
                        'statement': str(statement['choice_text']),
                        'type': str(statement['choice_result']),
                        'prompt_id': int(prompt['statement_number'])
                    }
                    statements.append(statement_schema)

            self.set_table_data(statements)
            self.insert_data_in_db()

    def group_by_prompt_id(self, prompt_id: int) -> dict:
        """Get all statements for a given prompt_id."""
        cursor = connect_db()
        qry = f"SELECT * FROM {self.table_name} WHERE prompt_id IS ?"
        try:
            cursor.execute(qry, (prompt_id,))
            data = [dict(row) for row in cursor.fetchall()]

            prompt_schema = {
                "prompt_id": prompt_id,
                "statements": [{
                    "statement_id": statement['id'],
                    "statement": statement['statement'],
                    "type": statement['type']} for statement in data]
            }
            return prompt_schema
        except Exception as e:
            print(e)
            return []
