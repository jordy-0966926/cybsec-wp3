from typing import List

import bcrypt
from src.lib.models.class_ import Class
from src.lib.models.database_entity import DatabaseEntry
from src.lib.util.database import db_cursor as connect_db
from src.lib.util.seed_data import students as student_json


class Teacher(DatabaseEntry):
    def __init__(self):
        super().__init__()
        self.table_name = 'teachers'
        self.ukey_name = 'id'

        self.is_authorized = False
        self.moderator = False
        self.data = None
        self.role_data = None

    def get_teachers(self) -> List[dict]:
        """Get the teachers."""
        teacher_ids = self.get_all_ids()
        return self.get_row_by_ids(ids=teacher_ids)

    @staticmethod
    def get_teacher_id_by_username(username: str) -> int:
        """Get the teacher id by username."""

        qry = "SELECT id FROM teachers WHERE username = ?"
        cursor = connect_db()
        cursor.execute(qry, (username,))
        teacher = cursor.fetchone()
        if teacher:
            return int(teacher['id'])
        else:
            return None

    def get_teacher_role(self) -> dict:
        """Get the teacher role."""
        qry = "SELECT is_admin FROM teachers WHERE id = ?"
        cursor = connect_db()
        cursor.execute(qry, (self.teacher_id,))
        applicant = dict(cursor.fetchone())
        if applicant:
            self.moderator = applicant['is_admin'] == 1
            teacher = self.get_row_by_ids(id=self.teacher_id)[0]
            return teacher
        return None

    def authenticate_teacher(self, username: str, password: str) -> bool:
        """Check the teacher credentials with bcrypt."""

        teacher_id = self.get_teacher_id_by_username(username)

        # Set the teacher_id attribute
        if teacher_id:
            self.teacher_id = teacher_id
            teacher = self.get_row_by_ids(id=teacher_id)[0]

            stored_password = teacher['password']

            # Verifieer het wachtwoord met bcrypt
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                self.is_authenticated = True
                self.data = teacher
                self.admin = bool(teacher['admin'])
                return True

        return False

    def seed_teachers(self, demo_size: int = 5) -> None:
        """Seed database with mock data for demo."""
        if self.get_table_count() == 0:
            teachers = []
            for i in range(1, demo_size + 1):
                username = f'test{i}'
                password = f'test{i}'

                # Generate a salt and hash the password
                salt = bcrypt.gensalt()
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

                teachers.append(
                    {"username": username, "password": hashed_password.decode('utf-8')})

            self.set_table_data(teachers)
            self.insert_data_in_db()


model_class = Class()


class Student(DatabaseEntry):
    def __init__(self):
        super().__init__()
        self.table_name = 'students'
        self.ukey_name = 'id'

        self.is_authenticated = False
        self.is_authorized = False
        self.data = None

    def seed_students(self):
        if self.get_table_count() == 0:
            students = []
            for student in student_json:
                student_schema = {
                    'student_num': str(student['student_number']),
                    'class_id': int(model_class.get_class_by_name(student['student_class'])['id']),
                    'name': str(student['student_name'])
                }
                students.append(student_schema)

            self.set_table_data(students)
            self.insert_data_in_db()

    def get_user_data_by_id(self, user_id: int) -> dict:
        """Get the user by id."""
        try:
            self.data = self.get_row_by_ids(id=user_id)[0]
            if self.data:
                return self.data
            else:
                return None

        except Exception as e:
            print(f"Error in get_user_data_by_id: {e}")
            return None

    @staticmethod
    def get_user_id_by_studentnum(student_num: str) -> int:
        """Get the user id by student_num."""

        qry = "SELECT id FROM students WHERE student_num IS ?"
        cursor = connect_db()
        cursor.execute(qry, (student_num,))
        user = cursor.fetchone()

        if user is not None:
            user_id = dict(user)['id']
            return user_id
        else:
            return None

    def authenticate_student(self, student_num: str) -> dict:
        """Check the user credentials."""

        user_id = self.get_user_id_by_studentnum(student_num)

        # Set the user_id attribute
        self.user_id = user_id

        if user_id:
            self.is_authenticated = True
            self.data = self.get_row_by_ids(id=user_id)[0]
            self.authorize_student()
            return True

        return None

    def authorize_student(self) -> None:
        try:
            qry = f"SELECT mbti FROM {self.table_name} WHERE id IS ?"
            cursor = connect_db()
            cursor.execute(qry, (self.user_id,))
            data = cursor.fetchone()

            # If user is found
            if data:
                if dict(data)['mbti']:
                    print(f"Student is authorized {dict(data)['mbti']}")
                    self.is_authorized = False
            else:
                print("Student is not authorized")
                self.is_authorized = True

        except Exception as e:
            print(f"Error in auth: {e}")

    def get_student_answers(self, student_id: int) -> List[dict]:
        """Get the student answers."""
        qry = "SELECT statement_id FROM answers WHERE student_id = ?"
        cursor = connect_db()
        cursor.execute(qry, (student_id,))

        answers = [row['statement_id'] for row in cursor.fetchall()]

        statement_prompt_ids = []
        for answer in answers:
            qry = "SELECT prompt_id FROM statements WHERE id = ?"
            cursor.execute(qry, (answer,))
            statement_prompt_ids.append(cursor.fetchone())

        student_answer = [{"prompt_id": statement_prompt_ids[i],
                           "statement_id": statement_prompt_ids[i]} for i in range(len(statement_prompt_ids))]

        return cursor.fetchall()
