from flask_login import current_user
from server.src.lib.models.database_entity import DatabaseEntry
from server.src.lib.util.database import db_cursor as connect_db

from typing import List


class Answer:
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

    def insert_answer(self, answers: list) -> None:
        """Insert an answer into the database."""
        student_id = current_user.user_id
        data = [{'statement_id': answer, 'student_id': student_id}
                for answer in answers]
        print(data)
