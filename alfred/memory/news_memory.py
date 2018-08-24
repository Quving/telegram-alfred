#!/usr/bin/env python
# -*- coding: utf-8 -*-

from alfred.memory.memory import Memory
from alfred.memory.user_memory import UserMemory


class NewsMemory(Memory):
    def __init__(self):
        self.alfred_user_memory = UserMemory()
        self.mongo_client = super(NewsMemory, self).get_mongo_client()
