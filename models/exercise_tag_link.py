from db import db


class ExerciseTagsLink(db.Model):
    __tablename__ = "exercise_tag_link"

    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"))
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"))