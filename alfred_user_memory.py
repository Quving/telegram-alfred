#!/usr/bin/env python3
import os
from alfred_exceptions import UserNotFoundException
from pymongo import MongoClient
from user import User


class AlfredUserMemory:
    def __init__(self):
        self.mongo = self.get_mongo_client()

    def get_mongo_client(self):
        """
        Returns a MongoClient object with the specified database host.

        :return:
        """
        mongo_host = os.getenv("ALFRED_MONGO_DB_HOST", "db")
        client = MongoClient("mongodb://" + mongo_host)

        return client

    def get_user_by_id(self, user_id):
        """
        Returns an object of instance User if exist.
        If not exist, raise UserNotFoundException
        :param user_id:
        :return:
        """
        id = str(user_id)

        user_db = self.mongo.alfred.user
        user_dict = user_db.find_one({"id": id})
        if user_dict is None:
            raise UserNotFoundException("User " + id + " does not exist.")

        user = User(user_dict=user_dict)
        return user

    def user_exist_by_id(self, id):
        """
        Returns true, if user exist. Else False.

        :param id:
        :return:
        """
        user_db = self.mongo.afred.user
        return not user_db.find_one({"id": str(id)}) is None

    def upsert_user(self, user):
        """
        Add user to db if user does not exist. Otherwise update the existing user."
        User will be identified by the id that is given by telegram.

        :return:
        """

        if not isinstance(user, User):
            raise ValueError("Expected user object. Given " + str(type(dict)))

        id = user.id
        user_dict = user.to_dict()

        user_db = self.mongo.alfred.user

        key = {"id": id}
        user_db.update(key, user_dict, upsert=True)