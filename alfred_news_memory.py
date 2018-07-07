#!/usr/bin/env python3
import os

from pymongo import MongoClient

from alfred_exceptions import UserNotFoundException
from alfred_user_memory import AlfredUserMemory
from user import User


class AlfredNewsMemory:
    def __init__(self):
        self.alfred_user_memory = AlfredUserMemory()

    def get_mongo_client(self):
        """
        Returns a MongoClient object with the specified database host.

        :return:
        """
        mongo_host = os.getenv("ALFRED_MONGO_DB_HOST", "db")
        client = MongoClient("mongodb://" + mongo_host)

        return client

    def get_neues(self, preferences):
        """
        Returns news in respect to the individual user preferences.
        :param user_id:
        :return:
        """

        # TODO Some processing with the stored preferences. Type of dict.

        return "In Bearbeitung! Kommt in Kuerze!"
