import os
from tempfile import mkdtemp

import joblib
from minio import Minio


class Storage:

    def __init__(self):
        self.__minio_client = Minio(os.getenv("MINIO.HOST"),
                                    access_key=os.getenv("MINIO.ACCESS-KEY"),
                                    secret_key=os.getenv("MINIO.SECRET-KEY"),
                                    secure=False)
        self.__bucket_name = 'models'

    def save_model(self, model, course_id, school_year, grade_item_position):
        local_filename = os.path.join(mkdtemp(), f'{course_id}-{school_year}-{grade_item_position}.joblib')
        minio_filename = f'/models/{course_id}/{school_year}-{grade_item_position}.joblib'
        joblib.dump(model, local_filename)
        with open(local_filename, 'rb') as file_data:
            file_stat = os.stat(local_filename)
            self.__minio_client.put_object(self.__bucket_name, minio_filename, file_data, file_stat.st_size)

    def load_model(self, course_id, school_year, grade_item_position):
        local_filename = os.path.join(mkdtemp(), f'{course_id}-{school_year}-{grade_item_position}.joblib')
        minio_filename = f'/models/{course_id}/{school_year}-{grade_item_position}.joblib'
        self.__minio_client.fget_object(self.__bucket_name, minio_filename, local_filename)
        return joblib.load(local_filename)
