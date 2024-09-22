from flask import Blueprint, jsonify, request

from server.src.lib.models.class_ import Class


blueprint = Blueprint('class_', __name__)

# model instances
model_class = Class()


@blueprint.route('/class', methods=['GET', 'POST'])
def class_():
    if request.method == "GET":

        data = model_class.get_rows()
        schema = []
        for row in data:
            schema.append({
                "id": row['id'],
                "name": row['name'],
            })

        return jsonify(schema)
