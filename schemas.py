from marshmallow import Schema, fields


class PlainExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)


class PlainWorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    time_of_day = fields.Str(required=True)
    body_weight = fields.Float(required=True)


class PlainSupplementSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    quantity = fields.Float(required=True)
    workout_id = fields.Int(load_only=True)
    timing = fields.String(required=True)


class PlainSeriesSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    exercise_name = fields.Str(dump_only=True)
    sets = fields.Int(required=True)

    s1_reps = fields.Int(load_only=True)
    s1_weight = fields.Int(load_only=True)
    s2_reps = fields.Int(load_only=True)
    s2_weight = fields.Int(load_only=True)
    s3_reps = fields.Int(load_only=True)
    s3_weight = fields.Int(load_only=True)
    s4_reps = fields.Int(load_only=True)
    s4_weight = fields.Int(load_only=True)
    s5_reps = fields.Int(load_only=True)
    s5_weight = fields.Int(load_only=True)

    mean_1rm = fields.Int(dump_only=True)


class ExerciseSchema(PlainExerciseSchema):
    tags = fields.List(fields.Nested(PlainTagSchema(), dump_only=True))


class TagSchema(PlainTagSchema):
    exercises = fields.List(fields.Nested(PlainExerciseSchema(), dump_only=True))


class WorkoutSchema(PlainWorkoutSchema):
    supplements = fields.List(fields.Nested(PlainSupplementSchema(), dump_only=True))
    series = fields.List(fields.Nested(PlainSeriesSchema(), dump_only=True))

