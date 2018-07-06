#!/usr/bin/env python3
import json


class User:
    def __init__(self, id):
        self.id = id
        self.other = {}
        self.username = ""
        self.first_name = ""


    def to_dict(self):
        data = {"id": self.id,
                "username": self.username,
                "first_name": self.first_name}

        return data


