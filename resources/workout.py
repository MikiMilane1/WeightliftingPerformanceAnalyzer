import uuid
from flask import Flask, request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import WorkoutModel
import datetime as dt
from schemas import WorkoutSchema, PlainWorkoutSchema
from sqlalchemy.exc import IntegrityError

blp = Blueprint("workout", __name__, description="Operations on workouts", url_prefix="/api")


@blp.route("/workout")
class Workout(MethodView):

    @blp.alt_response(404, description="Returned when a workout with that date already exists")
    @blp.response(200, WorkoutSchema, description="Returned when a workout is added to the DB")
    def post(self):
        workout_data = request.get_json()

        date = dt.date(
            year=workout_data["year"],
            month=workout_data["month"],
            day=workout_data["day"],
        )

        workout = WorkoutModel(
            date=date,
            body_weight=workout_data["body_weight"],
            h_of_sleep=workout_data["h_of_sleep"],
            time_of_day=workout_data["time_of_day"]
        )
        try:
            db.session.add(workout)
            db.session.commit()
            return workout
        except IntegrityError:
            abort(404, message="A workout with that date already exists.")


    @blp.response(200, PlainWorkoutSchema(many=True))
    def get(self):
        return WorkoutModel.query.all()


@blp.route("/workout/<string:workout_id>")
class Workout(MethodView):

    @blp.response(200, WorkoutSchema)
    def get(self, workout_id):
        workout = WorkoutModel.query.get(workout_id)
        if workout:
            return workout
        else:
            return {"message": "Workout with that id does not exist"}

    def delete(self, workout_id):
        workout = WorkoutModel.query.get(workout_id)
        if workout:
            db.session.delete(workout)
            db.session.commit()
            return {"message": "Workout deleted"}
        else:
            return {"message": "Workout with that id does not exist"}

    def put(self, workout_id):
        workout_data = request.get_json()
        workout = WorkoutModel.query.get(workout_id)

        if workout:
            date = dt.date(
                year=workout_data["year"],
                month=workout_data["month"],
                day=workout_data["day"],
            )
            workout.date = date
            workout.time_of_day = workout_data["time_of_day"]
            workout.body_weight = workout_data["body_weight"]
            workout.h_of_sleep = workout_data["h_of_sleep"]

            db.session.add(workout)
            db.session.commit()
            return {"message": "Workout updated successfully."}

        else:
            return {"message": "Workout with that id does not exist"}