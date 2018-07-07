#!/usr/bin/env python3

import os
import random

from pymongo import MongoClient

from alfred_user_memory import AlfredUserMemory


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

        tmp = []
        news_articles = client.alfred_db.test.find(preferences)

        for x in news_articles:
            tmp.append(x)

        index = 0
        if len(tmp) - 1 < 0:
            index = 0

        news_article = tmp[random.randint(0, index)]
        if len(tmp) == 0:
            return "Es gibt keine neuen Nachrichten mit ihren angegebenen Präferenzen."

        if "teaser" in news_article and "link" in news_article:
            text = news_article["teaser"] + "\n\n" + news_article["link"]
            return text
