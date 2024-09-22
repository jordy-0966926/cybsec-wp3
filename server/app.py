import flask
from flask import Flask, jsonify
from flask_jwt_extended import (JWTManager, create_access_token,
                                get_jwt_identity, jwt_required)
from src.api import blueprint as endpoints
from src.lib.models.class_ import Class
from src.lib.models.statement import Statement
from src.lib.models.user import Student, Teacher
from src.lib.util.database import db_check, db_create

model_class = Class()
model_statement = Statement()
model_student = Student()
model_teacher = Teacher()

# Check for database connection
if not db_check():
    db_create()

    # Seed database on first run
    model_teacher.seed_teachers()
    model_class.seed_classes()
    model_statement.seed_statements()
    model_student.seed_students()

# Disable sorting of JSON keys
flask.json.provider.DefaultJSONProvider.sort_keys = False

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

app.register_blueprint(endpoints)


if __name__ == "__main__":
    app.run(debug=True)
