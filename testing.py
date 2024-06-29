from db import db
from sqlalchemy import create_engine
db_url = "sqlite:///data.db"
from flask import Flask
from models.exercise import ExerciseModel
from models.supplements import SupplementModel
from models.workout import WorkoutModel
from models.series import SeriesModel
from models.tag import TagModel
from matplotlib import pyplot as plt
import pandas as pd
import os
from app import create_app
print("Engine created successfully!")

app = create_app()

with app.app_context():
    data = []
    series = SeriesModel.query.filter_by(exercise_id=2).all()
    for entry in series:
        data_entry = {
            "date": entry.workout.date,
            "1rm": entry.mean_1rm
        }
        data.append(data_entry)
    df = pd.DataFrame(data)
    plt.plot(df["date"], df["1rm"])

    output_dir = os.path.join("static", "assets", "img")
    filename = "343434.png"
    output_path = os.path.join(output_dir, filename)
    # os.makedirs(output_dir, exist_ok=True)
    plt.savefig(output_path)
    plt.close()
