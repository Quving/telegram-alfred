#!/usr/bin/env python3
import os

from pymongo import MongoClient


class Memory:
    def __init__(self):
        self.mongo_client = self.get_mongo_client()

    def get_mongo_client(self):
        """
        Returns a MongoClient object with the specified database host.

        :return:
        """
        mongo_host = os.getenv("ALFRED_MONGO_DB_HOST", "db")
        client = MongoClient("mongodb://" + mongo_host)

        return client
