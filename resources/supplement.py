from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PlainExerciseSchema, PlainSupplementSchema
from models import SupplementModel, WorkoutModel
from db import db
from flask_jwt_extended import jwt_required
from sqlalchemy import exc

blp = Blueprint("supplements", __name__, description="Operations on supplements", url_prefix="/api")


@blp.route("/supplement")
class Supplement1(MethodView):

    @jwt_required()
    @blp.arguments(PlainSupplementSchema)
    @blp.response(200, PlainSupplementSchema, description="Returned when supplement entry is created and appended to workout")
    def post(self, supp_data):
        supplement = SupplementModel(**supp_data)
        try:
            db.session.add(supplement)
            db.session.commit()
            return supplement
        except:
            db.session.rollback()
            return {"Error": "Not a valid supplement name"}

    @blp.response(200, PlainSupplementSchema(many=True))
    def get(self):
        return SupplementModel.query.all()


@blp.route("/supplement/<int:supp_id>")
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

    @jwt_required()
    @blp.arguments(PlainSupplementSchema)
    @blp.response(200, PlainSupplementSchema)
    def put(self, supp_data, supp_id):
        supplement = SupplementModel.query.get(supp_id)
        # valid_names = [enum_name for enum_name in SupplementModel.name.property.columns[0].type.enums]
        valid_names = ["citrulline", "caffeine", "creatine"]
        if supp_data["name"] not in valid_names:
            return {"Error": "Not a valid supplement name"}
        if supplement:
            supplement.name = supp_data["name"]
            supplement.quantity = supp_data["quantity"]
            supplement.timing = supp_data["timing"]
            supplement.workout_id = supp_data["workout_id"]
            db.session.add(supplement)
            db.session.commit()
            return supplement
