from db import db


class SupplementModel(db.Model):
    __tablename__ = "supplements"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Enum("creatine", "citrulline", "caffeine", name="supplement_name_enum"), nullable=False)
    quantity = db.Column(db.Float(precision=1), nullable=False)
    timing = db.Column(db.Enum("pre", "post", name="supplement_timing_enum"), nullable=False)

    # MANY TO ONE W/ WORKOUT
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), unique=False, nullable=False)
    workout = db.relationship("WorkoutModel", back_populates="supplements")


