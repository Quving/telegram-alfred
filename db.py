import os

from pymongo import MongoClient


class AlfredMemory:
    def __init__(self):
        self.mongo = self.get_mongo_client()

    def get_mongo_client(self):
        mongo_host = os.getenv("ALFRED_MONGO_DB_HOST", "db")
        client = MongoClient("mongodb://" + mongo_host)

        return client

    def upsert_user(self, user_id, data):
        """
        Add user to db if user does not exist. Otherwise update the existing user."
        User will be identified by the id that is given by telegram.

        :return:
        """
        id = str(user_id)
        user_db = self.mongo.alfred.user

        user = user_db.find_one({"id": id})

        if user is None:
            

        else:
            for key, value in data.items():
                user[key] = value

            key = {"id": id}
            user_db.update(key, data_new, upsert=True)
