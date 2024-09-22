from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from src.lib.models.user import Student

blueprint = Blueprint('student', __name__, template_folder='templates')

session_user = Student()


@blueprint.route('/student', methods=['GET', 'POST'])
def student_login():
    if request.method == "GET":
        return jsonify(session_user.data)

    if request.method == "POST":
        student_num = request.json.get('student_num')

        if session_user.authenticate_student(str(student_num)):
            access_token = create_access_token(identity=student_num)

            return jsonify(access_token=access_token, user_data=session_user.data)

        return jsonify({"message": "Invalid student credentials"}, 401)
