from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PlainExerciseSchema
from models import ExerciseModel, TagModel, WorkoutModel, SupplementModel
from db import db
from sqlalchemy.exc import IntegrityError

blp = Blueprint("testing", __name__, description="Testing", url_prefix="/api")


@blp.route('/testing')
class Testing(MethodView):

    def get(self):
        exercise = ExerciseModel.query.get(1)
        for item in exercise.tags:
            print(item.name)
        return {"message": "testing"}
