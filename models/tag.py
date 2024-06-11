from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10), nullable=False, unique=True)

    # MANY TO MANY W/ ExerciseModel
    exercises = db.relationship("ExerciseModel", back_populates="tags", secondary="exercise_tag_link")
