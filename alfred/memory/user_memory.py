#!/usr/bin/env python3

from alfred.exceptions import UserNotFoundException
from alfred.material.user import User
from alfred.memory.memory import Memory


class UserMemory(Memory):
    def __init__(self):
        super().__init__()
        self.user_db = self.db.user

    def get_user_by_id(self, user_id):
        """
        Returns an object of instance User if exist.
        If not exist, raise UserNotFoundException
        :param user_id:
        :return:
        """
        id = str(user_id)

        user_dict = self.user_db.find_one({"id": id})
        if user_dict is None:
            raise UserNotFoundException("User " + id + " does not exist.")

        user = User(user_dict=user_dict)
        return user

    def user_exist_by_id(self, user_id_str):
        """
        Returns true, if user exist. Else False.

        :param user_id_str:
        :return:
        """
        query = self.user_db.find_one({"id": user_id_str})
        return not query is None

    def upsert_user(self, user):
        """
        Add user to db if user does not exist. Otherwise update the existing user."
        User will be identified by the id that is given by telegram.

        :return:
        """

        if not isinstance(user, User):
            raise ValueError("Expected user object. Given " + str(type(dict)))

        id = user.id
        user_dict = user.to_dict()

        key = {"id": id}
        self.user_db.update(key, user_dict, upsert=True)
