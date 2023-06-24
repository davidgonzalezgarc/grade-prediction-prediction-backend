import pandas as pd

from db import Database
from storage import Storage

database = Database()
storage = Storage()


def load_student(course_id, school_year, grade_item_position, student_id):
    engine = database.get_engine()
    return pd.read_sql(database.get_predict_query(), engine,
                       params=(course_id, school_year, grade_item_position, student_id))


def predict(course_id, school_year, grade_item_position, student_id):
    model = storage.load_model(course_id, int(school_year) - 1, grade_item_position)
    student = load_student(course_id, school_year, grade_item_position, student_id)
    student_X = student.iloc[:, 0:-1]
    return model.predict(student_X)[0]
