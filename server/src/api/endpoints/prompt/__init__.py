from flask import Blueprint, jsonify, request

from server.src.lib.models.statement import Statement


blueprint = Blueprint('prompt', __name__)

# model instances
model_prompt = Statement()


@blueprint.route('/prompt/<prompt_id>', methods=['GET', 'POST'])
def prompt(prompt_id: int):
    if request.method == "GET":
        data = model_prompt.group_by_prompt_id(prompt_id)

        return (jsonify(data))


@blueprint.route('/prompt', methods=['GET', 'POST'])
def prompts():
    if request.method == "GET":
        schema = []
        prompt_count = model_prompt.get_table_count()/2

        for i in range(1, int(prompt_count)+1):
            schema.append(model_prompt.group_by_prompt_id(i))

        return jsonify(schema)
