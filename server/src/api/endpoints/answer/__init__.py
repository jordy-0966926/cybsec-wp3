from flask import Blueprint, jsonify, request
from src.lib.models.answer import Answer
from src.lib.models.user import Student

blueprint = Blueprint('answer', __name__)

# model instances
model_answer = Answer()
model_student = Student()


@blueprint.route('/answer', methods=['GET'])
def answer():
    if request.method == "GET":
        answer_id = request.args.get('id')
        if answer_id:
            return jsonify(model_answer.get_answer_by_id(answer_id), 200)
        return jsonify({"message": "No answer id provided"}, 401)


@blueprint.route('/answer/submit', methods=['GET', 'POST'])
def submit_answer():
    if request.method == "POST":
        data = request.json

        model_answer.insert_answer(data)
        # statement = data['statement']
        # type = data['type']
        # prompt_id = data['prompt_id']

        # if model_statement.insert_statement(statement, type, prompt_id):
        return jsonify({"status": "success", "message": "Statement submitted"}, 200)

        return jsonify({"message": "Error submitting statement"}, 401)
