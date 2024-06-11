from db import db
from models.exercise import ExerciseModel
from models.supplements import SupplementModel
from models.workout import WorkoutModel
from models.series import SeriesModel
from models.tag import TagModel

tag = TagModel.query.get(1)
print(tag)