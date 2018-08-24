#!/usr/bin/env python3

from alfred.memory import Memory
from alfred.user_memory import UserMemory


class NewsMemory(Memory):
    def __init__(self):
        self.alfred_user_memory = UserMemory()
        self.mongo_client = super(NewsMemory, self).get_mongo_client()
