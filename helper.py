#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

from telegram import ReplyKeyboardMarkup


class Helper():
    with open("cities.json", "r") as f:
        cities = json.load(f)

    @staticmethod
    def create_replykeyboardmarkup(args):
        """
        Creates a markup.
        :param args:
        :return: ReplyKeyboardMarkup
        """
        reply_keyboard = []
        if len(args) % 2 == 0:
            for i in range(0, len(args), 2):
                reply_keyboard.append([args[i], args[i + 1]])
        else:
            for i in range(0, len(args) - 1, 2):
                reply_keyboard.append([args[i], args[i + 1]])

            reply_keyboard.append([args[-1]])
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)
        return markup

    @staticmethod
    def cities_from_region(region):
        if not region in Helper.cities:
            return []
        else:
            return Helper.cities[region]
