from server.src.lib.models.database_entity import DatabaseEntry
from server.src.lib.util.database import db_cursor as connect_db
from typing import List
from server.src.lib.models.class_ import Class
from server.src.lib.util.seed_data import students as student_json


class Teacher(DatabaseEntry):
    def __init__(self):
        super().__init__()
        self.table_name = 'teachers'
        self.ukey_name = 'id'

        self.is_authorized = False
        self.moderator = False
        self.data = None
        self.role_data = None

        # Flask-Login required attributes
        self.is_active = True
        self.is_anonymous = False
        self.is_authenticated = False
        self.user_id = None

    def get_teachers(self) -> List[dict]:
        """Get the teachers."""
        teacher_ids = self.get_all_ids()
        return self.get_row_by_ids(ids=teacher_ids)

    def get_teacher_data_by_id(self, teacher_id: int) -> dict:
        """Get the teacher by id."""
        self.teacher_id = teacher_id

        if teacher_id is not None:
            teacher_role = self.get_teacher_role()
            if teacher_role:
                # Set either moderator or applicant role data as attribute
                self.is_authenticated = True
                self.role_data = teacher_role
                self.data = self.get_row_by_ids(id=teacher_id)[0]
                return True
        else:
            return None
        return self.get_row_by_ids(id=teacher_id)

    @staticmethod
    def get_teacher_id_by_teachername(teachername: str) -> int:
        """Get the teacher id by teachername."""

        qry = "SELECT id FROM teachers WHERE teachername = ?"
        cursor = connect_db()
        cursor.execute(qry, (teachername,))
        teacher = cursor.fetchone()
        if teacher is not None:
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

    def authenticate_teacher(self, teachername: str, password: str) -> dict:
        """Check the teacher credentials."""

        teacher_id = self.get_teacher_id_by_teachername(teachername)

        # Set the teacher_id attribute
        self.teacher_id = teacher_id

        if teacher_id is not None:
            teacher_role = self.get_teacher_role()
            if teacher_role['password'] == password:
                self.is_authenticated = True
                # Set either moderator or applicant role data as attribute
                self.role_data = teacher_role
                self.data = self.get_row_by_ids(id=teacher_id)[0]
                return True

        return None

    def demo(self, demo_size: int = 5) -> None:
        """Seed database with mock data for demo."""
        demo_data = [{"username": f'teacher{i}', "password": f'password{i}'}
                     for i in range(1, demo_size + 1)]
        if self.get_table_count() > 0:
            return
        self.set_table_data(demo_data)
        self.insert_data_in_db()

    # Flask-Login methods
    def get_id(self):
        """Return the teacher ID as a string."""
        return str(self.teacher_id)


model_class = Class()


class Student(DatabaseEntry):
    def __init__(self):
        super().__init__()
        self.table_name = 'students'
        self.ukey_name = 'id'

        self.is_authorized = False
        self.data = None

        # Flask-Login required attributes
        self.is_active = True
        self.is_anonymous = False
        self.is_authenticated = False
        self.user_id = None

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
            return int(user['id'])
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
            cursor.execute(qry, (self.user_id))
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

    # Flask-Login methods
    def get_id(self):
        """Return the user ID as a string."""
        return str(self.user_id)
