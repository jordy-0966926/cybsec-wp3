from flask import Blueprint, jsonify, request
from flask_login import login_user, current_user
from server.src.lib.models.user import Student


blueprint = Blueprint('student', __name__, template_folder='templates')

session_user = Student()


@blueprint.route('/student', methods=['GET', 'POST'])
def student_login():
    if request.method == "GET":

        if True:
            return jsonify({"status": "success", "message": "Student is authenticated", "data": {"student": session_user.data}}, 200)
        else:
            return jsonify({"message": "Invalid student credentials"}, 401)
    if request.method == "POST":
        data = request.json
        student_num = data['student_num']
        if session_user.authenticate_student(str(student_num)):
            login_user(session_user, remember=False)
            print(
                f"Student is authenticated { session_user.is_authorized}")
            return jsonify({"status": "success", "message": "Student is authenticated", "data": {"student": session_user.data}}, 200)

        return jsonify({"message": "Invalid student credentials"}, 401)
