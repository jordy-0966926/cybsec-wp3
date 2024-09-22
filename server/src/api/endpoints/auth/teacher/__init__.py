from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from src.lib.models.user import Teacher

blueprint = Blueprint('teacher', __name__, template_folder='templates')


@blueprint.route('/teacher', methods=['POST'])
def teacher_login():
    if request.method == 'POST':
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        print(username, password)
        if not username or not password:
            return jsonify({"message": "Username and password are required"}), 400

        session_user = Teacher()

        if session_user.authenticate_teacher(username, password):
            access_token = create_access_token(identity=username)
            return jsonify(access_token=access_token, username=username)
        else:
            return jsonify({"message": "Invalid credentials"}), 401
