from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PlainExerciseSchema, PlainSupplementSchema
from models import SupplementModel, WorkoutModel
from db import db
from flask_jwt_extended import jwt_required

blp = Blueprint("supplements", __name__, description="Operations on supplements", url_prefix="/api")


@blp.route("/supplement")
class Supplement1(MethodView):

    @jwt_required()
    @blp.arguments(PlainSupplementSchema)
    @blp.response(200, PlainSupplementSchema, description="Returned when supplement entry is created and appended to workout")
    def post(self, supp_data):
        supplement = SupplementModel(**supp_data)
        db.session.add(supplement)
        db.session.commit()
        return supplement

    # @blp.response(200, PlainSupplementSchema(many=True))
    def get(self):
        return {"message": "test"}


@blp.route("/supplement/<string:supp_id>")
class Supplement2(MethodView):

    @blp.response(200, PlainSupplementSchema)
    def get(self, supp_id):
        supplement = SupplementModel.query.get(supp_id)
        if supplement:
            return supplement
        else:
            return {"Error": "Invalid supplement entry id."}

    @jwt_required()
    def delete(self, supp_id):
        supplement = SupplementModel.query.get(supp_id)
        if supplement:
            db.session.delete(supplement)
            db.session.commit()
            return {"Message": "Supplement entry deleted"}
        else:
            return {"Error": "Invalid supplement entry id."}
