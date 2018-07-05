#!/usr/bin/env python3

class BotTokenNotSetException(Exception):
    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)
