import os

from sqlalchemy import create_engine


class Database:

    def __init__(self):
        self.__db_url_connection = os.getenv("DB.URL")

    def get_engine(self):
        return create_engine(self.__db_url_connection)

    def get_train_query(self):
        return "CALL DATASET(%s, NULL, %s, NULL)"

    def get_predict_query(self):
        return "CALL DATASET(%s, %s, %s, %s)"
