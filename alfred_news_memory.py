#!/usr/bin/env python3
import os

from pymongo import MongoClient

from alfred_exceptions import UserNotFoundException
from alfred_user_memory import AlfredUserMemory
from user import User


class AlfredNewsMemory:
    def __init__(self):
        self.alfred_user_memory = AlfredUserMemory()

    def get_neues(self, preferences):
        """
        Returns news in respect to the individual user preferences.
        :param user_id:
        :return:
        """
        client = MongoClient("mongodb://" + os.getenv("ALFRED_MONGO_DB_HOST", "db"))
        news_article = client.alfred_db.test.find_one(preferences)
        client.close()
        return news_article

        # TODO Some processing with the stored preferences. Type of dict.

        return "In Bearbeitung! Kommt in Kuerze!"
