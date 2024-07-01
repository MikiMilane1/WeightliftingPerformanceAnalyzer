from flask import Blueprint, render_template
import os
from models.workout import WorkoutModel
from models.exercise import ExerciseModel
from models.series import SeriesModel
import matplotlib.pyplot as plt
import pandas as pd
import os

APP_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_PATH = os.path.join(APP_PATH, "templates")

blp = Blueprint("graphs", __name__, template_folder=TEMPLATE_PATH)


@blp.route("/plots/<int:exercise_id>")
def graphs(exercise_id):

    exercise = ExerciseModel.query.get(exercise_id)
    if exercise:
        series = SeriesModel.query.filter_by(exercise_id=exercise_id).all()
        data = []
        for entry in series:
            data_entry = {
                "date": entry.workout.date,
                "1rm": entry.mean_1rm,
                          }
            data.append(data_entry)
        print(data)
        df = pd.DataFrame(data)

        plt.figure(figsize=(10, 6))
        plt.plot(df["date"], df["1rm"])
        plt.xticks(rotation=90, fontsize=10)
        plt.subplots_adjust(bottom=0.25)
        plt.title(f'Mean one rep max recorded by date for exercise: {exercise.name}')
        plt.xlabel("Date")
        plt.ylabel("Mean 1RM [kg]")
        plt.tight_layout(pad=3)

        output_dir = os.path.join("static", "assets", "img")
        filename = "plot.png"
        output_path = os.path.join(output_dir, filename)
        plt.savefig(output_path)
        plt.close()
        return render_template('plots.html', exercise=exercise)
    else:
        return 'Invalid exercise id'
