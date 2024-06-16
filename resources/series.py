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


    @blp.response(200, PlainSeriesSchema)
    def get(self):
        return SeriesModel.query.all()

    @jwt_required()
    @blp.arguments(PlainSeriesSchema)
    @blp.response(200, PlainSeriesSchema)
    def post(self, series_data):
        series = SeriesModel(**series_data)
        db.session.add(series)
        db.session.commit()
        return series


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
    def put(self, series_id):
        series_data = request.get_json()
        series = SeriesModel.query.get(series_id)
        if series:
            series = SeriesModel(**series_data)
            db.session.add(series)
            db.session.commit()
            return series
        else:
            return {"Error": "Invalid series id"}


@blp.route("/workout/series")
class Series3(MethodView):

    def delete(self):
        raise NotImplementedError

