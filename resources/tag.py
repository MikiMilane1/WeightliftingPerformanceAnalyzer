from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import PlainTagSchema, TagSchema
from models import TagModel, ExerciseModel
from db import db
from flask import request
from sqlalchemy.exc import IntegrityError

blp = Blueprint("tag", __name__, description="Operations on tags", url_prefix="/api")


@blp.route("/tag")
class Tag1(MethodView):

    def post(self):
        tag_data = request.get_json()
        tag = TagModel(**tag_data)
        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            return {"message": "Tag with that name already exists"}
        return {"message": "Tag created successfully"}

    @blp.response(200, TagSchema(many=True))
    def get(self):
        # tag_list = [{"id": item.id,
        #              "name": item.name,
        #              # "exercises": item.exercises
        #              } for item in TagModel.query.all()]
        # return {"Tags": tag_list}
        return TagModel.query.all()


@blp.route("/tag/<string:tag_id>")
class Tag2(MethodView):

    def get(self, tag_id):
        tag = TagModel.query.get(tag_id)
        if tag:
            return {"Tag name": f"{tag.name}"}
        else:
            return {"Error": "Invalid tag id"}

    def delete(self, tag_id):
        tag = TagModel.query.get(tag_id)
        if tag:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted succesfully."}
        else:
            return {"Error": "Invalid tag id"}

    def put(self, tag_id):
        tag_data = request.get_json()
        tag = TagModel.query.get(tag_id)
        if tag:
            tag = TagModel(**tag_data)
            return {"message": "Tag updated succesfully."}
        else:
            return {"Error": "Invalid tag id"}


@blp.route("/exercise/<string:ex_id>/tag/<string:tag_id>")
class Tag3(MethodView):

    def post(self, ex_id, tag_id):

        exercise = ExerciseModel.query.get(ex_id)
        if exercise:
            tag = TagModel.query.get(tag_id)
            if tag:
                exercise.tags.append(tag)
                db.session.commit()
            else:
                return {"Error": "Invalid tag id"}
        else:
            return {"Error": "Invalid exercise id"}
        return {"message": "Tag appended successfully"}

    def delete(self, ex_id, tag_id):

        exercise = ExerciseModel.query.get(ex_id)
        if exercise:
            tag = TagModel.query.get(tag_id)
            if tag:
                exercise.tags.remove(tag)
                db.session.commit()
            else:
                return {"Error": "Invalid tag id"}
        else:
            return {"Error": "Invalid exercise id"}
        return {"message": "Tag removed from exercise succesfully"}