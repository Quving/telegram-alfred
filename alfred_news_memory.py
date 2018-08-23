#!/usr/bin/env python3

import os
import random

from pymongo import MongoClient
from alfred_memory import AlfredMemory
from alfred_user_memory import AlfredUserMemory


class AlfredNewsMemory(AlfredMemory):
    def __init__(self):
        self.alfred_user_memory = AlfredUserMemory()
        self.mongo_client = super(AlfredNewsMemory, self).get_mongo_client()
