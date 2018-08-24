#!/usr/bin/env python
# -*- coding: utf-8 -*-

from alfred.memory.memory import Memory


class NewsMemory(Memory):
    def __init__(self):
        super().__init__()
        self.news_db = self.db.news
