import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.model_selection import cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from db import Database
from storage import Storage

database = Database()
storage = Storage()


def load_dataset(course_id, grade_item_position):
    engine = database.get_engine()
    return pd.read_sql(database.get_train_query(), engine, params=(course_id, grade_item_position))


def preprocess_and_train(X, y):
    drop_cols = [
        "id",
        "course_id",
        "school_year",
        "student_id",
    ]
    cat_cols = [
        "address",
        "extra_curricular_activities",
        "family_size",
        "father_job",
        "mother_job",
        "parents_status",
        "romantic_relationship",
        "sex",
        "extra_educational_support",
        "extra_paid_classes",
        "family_educational_support",
    ]
    num_cols = [
        "age",
        "father_education",
        "free_time",
        "go_out",
        "health_status",
        "mother_education",
        "weekend_alcohol",
        "workday_alcohol",
        "absences",
        "failures",
        "travel_time",
        "weekly_study_time",
    ]
    for column in X.columns.values.tolist():
        if "grade_item" in column:
            num_cols.append(column)

    encoder = OneHotEncoder()
    scaler = StandardScaler()

    # model = RandomForestRegressor(max_depth=6)
    model = GradientBoostingRegressor(max_depth=3, n_estimators=70, learning_rate=0.06, random_state=8)

    transformer = ColumnTransformer([
        ('drop_cols', "drop", drop_cols),
        ('cat_cols', encoder, cat_cols),
        ('num_cols', scaler, num_cols)])

    pipe = Pipeline([("preprocessing", transformer),
                     ("regressor", model)])
    pipe.fit(X, y)
    return pipe


def score(model, X, y):
    scores = cross_validate(model, X, y, cv=5,
                            scoring=('r2', 'neg_mean_absolute_error', 'neg_mean_squared_error'),
                            return_train_score=True)
    r2 = np.mean(scores['test_r2'])
    print("r2", r2)
    mae = np.mean(np.abs(scores['test_neg_mean_absolute_error']))
    print("mae", mae)
    rmse = np.sqrt(np.mean(np.abs(scores['test_neg_mean_squared_error'])))
    print("rmse", rmse)


def create_model(course_id, school_year, grade_item_position):
    df = load_dataset(course_id, grade_item_position)

    df_X = df.iloc[:, 0:-1]
    df_y = df.iloc[:, -1]

    model = preprocess_and_train(df_X, df_y)

    print("score of course " + course_id + ", grade item pos " + grade_item_position)
    score(model, df_X, df_y)

    storage.save_model(model, course_id, school_year, grade_item_position)
