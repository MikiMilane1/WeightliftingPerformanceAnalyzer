from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PlainExerciseSchema, PlainSeriesSchema
from models import SeriesModel, WorkoutModel
from db import db
from flask_jwt_extended import jwt_required

blp = Blueprint("series", __name__, description="Operations on series", url_prefix="/api")


@blp.route("/series")
class Series1(MethodView):

    @blp.response(200, PlainSeriesSchema(many=True))
    def get(self):
        print('should be returning all series')
        return SeriesModel.query.all()

    @jwt_required()
    @blp.arguments(PlainSeriesSchema)
    @blp.response(200, PlainSeriesSchema)
    def post(self, series_data):
        series = SeriesModel(**series_data)
        db.session.add(series)
        db.session.commit()
        return series

    # TODO create put request for editing series


@blp.route("/series/<string:series_id>")
class Series2(MethodView):

    @blp.alt_response(404, description="Returned if the series with that id does not exist")
    @blp.response(200, PlainSeriesSchema)
    def get(self, series_id):
        series = SeriesModel.query.get(series_id)
        if series:
            return series
        else:
            abort(404, message="Invalid series id.")

    @jwt_required()
    @blp.response(404, description="Returned if the series with that id does not exist")
    def delete(self, series_id):
        series = SeriesModel.query.get(series_id)
        if series:
            db.session.delete(series)
            db.session.commit()
            return {"Message": "Series deleted successfully."}
        else:
            abort(404, message="Invalid series id.")

    @jwt_required()
    @blp.arguments(PlainSeriesSchema)
    @blp.response(200, PlainSeriesSchema)
    def put(self, series_data, series_id):
        series = SeriesModel.query.get(series_id)
        if series:
            series.exercise_id = series_data["exercise_id"]
            series.workout_id = series_data["workout_id"]
            series.sets = series_data["sets"]
            series.s1_reps = series_data["s1_reps"]
            series.s1_weight = series_data["s1_weight"]
            series.s2_reps = series_data["s2_reps"]
            series.s2_weight = series_data["s2_weight"]
            series.s3_reps = series_data["s3_reps"]
            series.s3_weight = series_data["s3_weight"]
            series.s4_reps = series_data["s4_reps"]
            series.s4_weight = series_data["s4_weight"]
            series.s5_reps = series_data["s5_reps"]
            series.s5_weight = series_data["s5_weight"]
            db.session.add(series)
            db.session.commit()
            return series
        else:
            return {"Error": "Invalid series id"}


@blp.route("/workout/series")
class Series3(MethodView):

    def delete(self):
        raise NotImplementedError
