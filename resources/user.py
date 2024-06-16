from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import UserSchema
from models import UserModel, ExpiredJTIModel
from db import db
from flask import request
from sqlalchemy.exc import IntegrityError
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

blp = Blueprint("user", __name__, description="Operations on tags", url_prefix="/api")


@blp.route("/register")
class UserRegister(MethodView):

    @blp.arguments(UserSchema)
    @blp.response(200, UserSchema)
    def post(self, user_data):
        user = UserModel(
            username=user_data["username"],
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        db.session.add(user)
        db.session.commit()
        return user


@blp.route("/login")
class UserLogin(MethodView):

    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data["username"]
        ).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            return {"access_token": access_token}


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        expired_jti = ExpiredJTIModel(jti=jti)
        db.session.add(expired_jti)
        db.session.commit()
        return {"message": "Succesfully logged out"}
