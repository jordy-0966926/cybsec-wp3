from flask import Blueprint, request, jsonify
from server.src.api.endpoints.auth.student import blueprint as student
from server.src.api.endpoints.auth.teacher import blueprint as teacher

from server.src.lib.models.user import Student, Teacher

blueprint = Blueprint('auth', __name__, url_prefix='/auth')

blueprint.register_blueprint(student)
blueprint.register_blueprint(teacher)

model_student = Student()
model_teacher = Teacher()


@blueprint.route('/session', methods=['GET', 'POST'])
def auth():
    if request.method == "GET":

        if model_student.is_authenticated:
            return jsonify({"status": "success", "message": "User is authenticated", "data": {"user": "test"}}, 200)

        else:
            return jsonify({"message": "Invalid credentials"}, 401)
