#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os


class Conts:
    MONGO_DB_HOST = os.getenv("ALFRED_MONGO_DB_HOST")
    ALFRED_BOT_TOKEN = os.getenv("ALFRED_BOT_TOKEN")
    DATENSCHUTZ_JSON = "files/datenschutz.json"
    HELPER_JSON = "files/help.json"
    CITIES_JSON = "files/cities.json"
