from flask import Flask, request
from flask_smorest import Api
from db import db
from resources.exercise import blp as ExerciseBlueprint
from resources.workout import blp as WorkoutBlueprint
from resources.tag import blp as TagBlueprint
from resources.supplement import blp as SupplementBluePrint
from resources.series import blp as SeriesBluePrint
from resources.testing import blp as TestingBluePrint


def create_app(db_url=None):
    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Workouts REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or "sqlite:///data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    api = Api(app)
    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return "Weightlifting app, homes"

    api.register_blueprint(ExerciseBlueprint)
    api.register_blueprint(WorkoutBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(SupplementBluePrint)
    api.register_blueprint(SeriesBluePrint)
    api.register_blueprint(TestingBluePrint)

    return app
