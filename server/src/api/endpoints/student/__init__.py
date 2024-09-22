from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from src.lib.models.answer import Answer
from src.lib.models.user import Student

blueprint = Blueprint('student', __name__)

# model instances
model_student = Student()
model_answer = Answer()


@blueprint.route('/student', methods=['GET', 'POST'])
def students():
    if request.method == "GET":
        data = model_student.get_rows()
        schema = []
        for row in data:
            schema.append({
                "id": row['id'],
                "student_num": row['student_num'],
                "type": row['mbti'],
                "class": row['class_id'],
                "team": row['team_id'],
            })

        return jsonify(schema)


@blueprint.route('/student/answers', methods=['GET', 'POST'])
@jwt_required()
def student_answers():
    if request.method == "GET":
        current_user = get_jwt_identity()
        student_id = model_student.get_user_id_by_studentnum(current_user)
        data = model_answer.get_answers_by_student_id(student_id=student_id)
        return jsonify(data)

    if request.method == "POST":
        student_id = request.json.get('student_id')
        statement_id = request.json.get('statement_id')
        pompt_id = request.json.get('prompt_id')
        model_answer.insert_answer(
            statement_id=statement_id, student_id=student_id, prompt_id=pompt_id)

        if not student_id or not statement_id:
            return jsonify({"message": "Student ID and Statement ID are required"}), 400

    return jsonify({"message": "Student answers received"}), 200
