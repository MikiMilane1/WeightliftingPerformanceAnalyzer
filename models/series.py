from db import db


class SeriesModel(db.Model):
    __tablename__ = "series"

    id = db.Column(db.Integer, primary_key=True)
    sets = db.Column(db.Integer, nullable=False)

    s1_reps = db.Column(db.Integer, nullable=True)
    s1_weight = db.Column(db.Integer, nullable=True)

    s2_reps = db.Column(db.Integer, nullable=True)
    s2_weight = db.Column(db.Integer, nullable=True)

    s3_reps = db.Column(db.Integer, nullable=True)
    s3_weight = db.Column(db.Integer, nullable=True)

    s4_reps = db.Column(db.Integer, nullable=True)
    s4_weight = db.Column(db.Integer, nullable=True)

    s5_reps = db.Column(db.Integer, nullable=True)
    s5_weight = db.Column(db.Integer, nullable=True)

    # MANY TO ONE W/ ExerciseModel
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), unique=False, nullable=False)
    # exercise_name = db.Column(db.String, db.ForeignKey("exercises.name"), unique=False, nullable=False)
    exercise = db.relationship("ExerciseModel", back_populates="series")

    # MANY TO ONE W/ WorkoutModel
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), unique=False, nullable=False)
    workout = db.relationship("WorkoutModel", back_populates="series")

    @property
    def exercise_name(self):
        return self.exercise.name

    @property
    def s1_1rm(self):
        s1_1rm = self.s1_weight / (1.0278 - 0.0278 * self.s1_reps)
        return s1_1rm

    @property
    def s2_1rm(self):
        s2_1rm = self.s2_weight / (1.0278 - 0.0278 * self.s2_reps)
        return s2_1rm

    @property
    def s3_1rm(self):
        s3_1rm = self.s3_weight / (1.0278 - 0.0278 * self.s3_reps)
        return s3_1rm

    @property
    def s4_1rm(self):
        s4_1rm = self.s4_weight / (1.0278 - 0.0278 * self.s4_reps)
        return s4_1rm

    @property
    def s5_1rm(self):
        s5_1rm = self.s5_weight / (1.0278 - 0.0278 * self.s5_reps)
        return s5_1rm

    @property
    def mean_1rm(self):
        return round((self.s1_1rm + self.s2_1rm + self.s3_1rm + self.s4_1rm + self.s5_1rm) / self.sets, 0)



