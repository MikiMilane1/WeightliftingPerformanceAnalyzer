import os

from flask import Flask, request, jsonify
from flask_smorest import Api
from db import db
from resources.exercise import blp as ExerciseBlueprint
from resources.workout import blp as WorkoutBlueprint
from resources.tag import blp as TagBlueprint
from resources.supplement import blp as SupplementBluePrint
from resources.series import blp as SeriesBluePrint
from resources.testing import blp as TestingBluePrint
from resources.user import blp as UserBluePrint
from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask import jsonify

from models import ExpiredJTIModel


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

    # Configure jwt
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=3)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=2)

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        blocklist = [item.jti for item in ExpiredJTIModel.query.all()]
        return jwt_payload["jti"] in blocklist

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ), 401
        )

    @jwt.additional_claims_loader
    def add_claims_to_jwt(identity):
        if identity == 1:
            return {"is_admin": True}
        else:
            return {"is_admin": False}

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed", "error": "invalid_token"}
            ), 401
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token",
                    "error": "authorization_required"
                }
            ), 401
        )


    # TODO store login credentials and jti blocklist in separate database
    with app.app_context():
        db.create_all()

    @app.route("/")
    def home():
        return "Weightlifting app, home"

    api.register_blueprint(ExerciseBlueprint)
    api.register_blueprint(WorkoutBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(SupplementBluePrint)
    api.register_blueprint(SeriesBluePrint)
    api.register_blueprint(TestingBluePrint)
    api.register_blueprint(UserBluePrint)

    return app
