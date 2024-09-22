import flask
from flask_login import LoginManager
from flask import Flask

from server.src.lib.util.database import db_check, db_create

from server.src.lib.models.user import Teacher
from server.src.lib.models.user import Student
from server.src.lib.models.class_ import Class
from server.src.lib.models.statement import Statement

from server.src.api import blueprint as endpoints

model_class = Class()
model_statement = Statement()
model_student = Student()

# Check for database connection
if not db_check():
    db_create()
    # Seed database on first run
    model_class.seed_classes()
    model_statement.seed_statements()
    model_student.seed_students()

# Disable sorting of JSON keys
flask.json.provider.DefaultJSONProvider.sort_keys = False

app = Flask(__name__)
app.secret_key = 'super secret key'

login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(endpoints)


@login_manager.user_loader
def load_user(user_id):
    session_user = Student()
    session_user.get_user_data_by_id(user_id)
    return session_user


if __name__ == "__main__":
    app.run(debug=True)
