from flask import Blueprint, jsonify, request
from src.lib.models.statement import Statement

blueprint = Blueprint('statement', __name__)

# model instances
model_statement = Statement()


@blueprint.route('/statement', methods=['GET', 'POST'])
def statements():
    if request.method == "GET":

        data = model_statement.get_rows()
        schema = []
        for row in data:
            schema.append({
                "id": row['id'],
                "statement": row['statement'],
                "type": row['type'],
                "prompt_id": row['prompt_id']
            })

        return jsonify(schema)
