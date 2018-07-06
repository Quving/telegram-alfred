#!/usr/bin/env python3


class User:
    def __init__(self, user_dict=None):
        self.user_dict = user_dict
        self.id = self.__get_user_dict_attribute(key="id", default="")
        self.username = self.__get_user_dict_attribute(key="username", default="")
        self.first_name = self.__get_user_dict_attribute(key="first_name", default="")
        self.preferences = self.__get_user_dict_attribute(key="preferences", default={})


    def __get_user_dict_attribute(self, key, default=None):
        """
        Return a value from the user_dict.
        If not exist, return default.

        :param key:
        :param default:
        :return:
        """
        if not key in self.user_dict:
            return default
        else:
            return self.user_dict[key]


    def to_dict(self):
        """
        Returns a dictionary object that represent the User object.
        :return:
        """
        data = {"id": self.id,
                "username": self.username,
                "first_name": self.first_name,
                "preferences": self.preferences}

        return data


