from typing import List

from flask_jwt_extended import get_jwt_identity
from src.lib.models.database_entity import DatabaseEntry
from src.lib.util.database import db_cursor as connect_db


class Answer(DatabaseEntry):
    def __init__(self):
        super().__init__()
        self.table_name = 'answers'
        self.ukey_name = 'id'

    def get_answer_by_id(self, answer_id: int) -> int:
        """Get the answer by id."""
        qry = f"SELECT answer FROM {self.table_name} WHERE id IS ?"
        cursor = connect_db()
        cursor.execute(qry, (answer_id,))
        data = cursor.fetchone()
        return dict(data)

    def get_answers_by_student_id(self, student_id: int) -> List[dict]:
        """Get the answers by student id."""
        qry = f"SELECT * FROM {self.table_name} WHERE student_id IS ?"
        cursor = connect_db()
        cursor.execute(qry, (str(student_id),))
        data = [dict(row) for row in cursor.fetchall()]
        return data

    def insert_answer(self, statement_id: int, student_id: int, prompt_id: int) -> None:
        """Insert an answer into the database."""
        data = [{'statement_id': statement_id,
                 'student_id': student_id,
                 'prompt_id': prompt_id}]
        print(data)
        self.set_table_data(data)
        self.insert_data_in_db()
