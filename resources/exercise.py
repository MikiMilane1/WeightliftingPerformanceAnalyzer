from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ExerciseSchema
from models import ExerciseModel
from db import db
from sqlalchemy.exc import IntegrityError

blp = Blueprint("exercises", __name__, description="Operations on exercises", url_prefix="/api")


@blp.route("/exercise")
class Exercise1(MethodView):

    @blp.response(200, ExerciseSchema(many=True))
    def get(self):
        return ExerciseModel.query.all()

    @blp.alt_response(400, description="Returned if the exercise with that name already exists.")
    @blp.response(200, ExerciseSchema)
    def post(self):
        exercise_data = request.get_json()
        exercise = ExerciseModel(**exercise_data)
        try:
            db.session.add(exercise)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Exercise with that name already exists in the database.")
        return exercise


@blp.route("/exercise/<string:exercise_id>")
class Exercise2(MethodView):

    @blp.response(200, ExerciseSchema)
    @blp.alt_response(404, description="Returned if the exercise with that id does not exist.")
    def get(self, exercise_id):
        exercise = ExerciseModel.query.get(exercise_id)
        if exercise:
            return exercise
        else:
            abort(404, message="There is no exercise with that id.")

    @blp.alt_response(404, description="Returned if the exercise with that id does not exist.")
    def delete(self, exercise_id):
        exercise = ExerciseModel.query.get(exercise_id)
        if exercise:
            db.session.delete(exercise)
            db.session.commit()
            return {"Message": "Exercise deleted succesfully."}
        else:
            abort(404, message="Invalid exercise id.")

    @blp.alt_response(404, description="Returned if the exercise with that id does not exist.")
    @blp.response(200, ExerciseSchema)
    def put(self, exercise_id):
        exercise_data = request.get_json()
        exercise = ExerciseModel.query.get(exercise_id)
        if exercise:
            exercise.name = exercise_data["name"]
        else:
            abort(404, message="Invalid exercise id.")
        db.session.add(exercise)
        db.session.commit()
        return exercise
