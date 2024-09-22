from flask import Blueprint, jsonify, request


blueprint = Blueprint('ping', __name__)


@blueprint.route('/ping', methods=['GET', 'POST'])
def ping():
    if request.method == "GET":

        return jsonify({"message": "pong"})

    if request.method == "POST":
        request_data = request.get_json()
        print(request_data)
        return jsonify({"message": "pong"}, 200)
