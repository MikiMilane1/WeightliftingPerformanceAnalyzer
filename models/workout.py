from db import db


class WorkoutModel(db.Model):
    __tablename__ = "workouts"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False, unique=True)
    time_of_day = db.Column(db.Enum("morning", "evening", name="time_of_day_enum"))
    body_weight = db.Column(db.Float(precision=1), nullable=False)
    h_of_sleep = db.Column(db.Float(precision=1), nullable=False)

    # ONE TO MANY W/ ExerciseInstanceModel
    series = db.relationship("SeriesModel", back_populates="workout", lazy="dynamic", cascade='all, delete')

    # ONE TO MANY W/ SupplementModel
    supplements = db.relationship("SupplementModel", back_populates="workout", lazy="dynamic", cascade='all, delete')