from flask import Blueprint, jsonify, request

from server.src.lib.models.user import Student


blueprint = Blueprint('student', __name__)

# model instances
model_student = Student()


@blueprint.route('/student', methods=['GET', 'POST'])
def students():
    if request.method == "GET":
        data = model_student.get_rows()
        schema = []
        for row in data:
            schema.append({
                "id": row['id'],
                "student_num": row['student_num'],
                "name": row['name'],
                "type": row['mbti'],
                "class": row['class_id'],
                "team": row['team_id'],
            })

        return jsonify(schema)
