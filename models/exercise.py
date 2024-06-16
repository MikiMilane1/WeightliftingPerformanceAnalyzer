from db import db


class ExerciseModel(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    # MANY TO MANY W/ TagModel
    tags = db.relationship("TagModel", back_populates="exercises", secondary="exercise_tag_link")

    # ONE TO MANY W/ SeriesModel
    series = db.relationship("SeriesModel", back_populates="exercise", lazy="dynamic", cascade="all, delete")


