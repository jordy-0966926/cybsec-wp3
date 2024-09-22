from flask import Blueprint

from server.src.api.endpoints.ping import blueprint as ping
from server.src.api.endpoints.statement import blueprint as statement
from server.src.api.endpoints.prompt import blueprint as prompt
from server.src.api.endpoints.class_ import blueprint as class_
from server.src.api.endpoints.auth import blueprint as auth
from server.src.api.endpoints.answer import blueprint as answer
from server.src.api.endpoints.student import blueprint as student

blueprint = Blueprint('api', __name__, url_prefix='/api')

blueprint.register_blueprint(ping)
blueprint.register_blueprint(statement)
blueprint.register_blueprint(prompt)
blueprint.register_blueprint(class_)
blueprint.register_blueprint(auth)
blueprint.register_blueprint(answer)
blueprint.register_blueprint(student)
