#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from pymongo import MongoClient

from alfred.vars import Conts


class Memory:
    def __init__(self):
        mongo_client = self.get_mongo_client()
        self.db = mongo_client[Conts.ALFRED_DB_NAME]

    def get_db(self):
        """
        Return the database name dependent from the current Alfred_mode.
        :return:
        """
        return self.db

    def get_mongo_client(self):
        """
        Returns a MongoClient object with the specified database host.

        :return:
        """
        mongo_host = os.getenv("ALFRED_MONGO_DB_HOST", "db")
        client = MongoClient("mongodb://" + mongo_host)

        return client
