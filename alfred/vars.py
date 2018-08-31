#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from alfred.exceptions import UnknownAlfredModeException


def get_mongo_db():
    """
    Return the name of the database in mongo.
    :return: str
    """
    key = "ALFRED_MODE"
    if os.getenv(key) == "production":
        return "alfred_prod"
    elif os.getenv(key) == "development":
        return "alfred_dev"
    else:
        raise UnknownAlfredModeException("Please set {}. Either 'production', or 'development'.".format(key))


class Conts:
    MONGO_DB_HOST = os.getenv("ALFRED_MONGO_DB_HOST")
    ALFRED_DB_NAME = get_mongo_db()
    ALFRED_BOT_TOKEN = os.getenv("ALFRED_BOT_TOKEN")
    DATENSCHUTZ_JSON = "files/datenschutz.json"
    HELPER_JSON = "files/help.json"
    CITIES_JSON = "files/cities.json"
