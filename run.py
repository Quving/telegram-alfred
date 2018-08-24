#!/usr/bin/env python3

from alfred import Alfred
import os
from alfred_exceptions import BotTokenNotSetException, DatabaseNotSetException


def check_envs():
    """
    Check if the required envs are set. It does not check, if the value has been set properly.
    :return:
    """
    alfred_bot_token = "ALFRED_BOT_TOKEN"
    if not os.getenv(alfred_bot_token):
        error = "Please set {}. If you do not possess one, request one from BotFather (@botfather in Telegram)." \
            .format(alfred_bot_token)
        raise BotTokenNotSetException(error)

    alfred_mongo_db = "ALFRED_MONGO_DB_HOST"
    if not os.getenv(alfred_mongo_db):
        error = "Please set {}. Required is a mongo-db to store user informations as well as cached files." \
            .format(alfred_mongo_db)
        raise DatabaseNotSetException(error)


if __name__ == "__main__":
    # Run checks.
    check_envs()

    # Launch 'Alfred'.
    alfred = Alfred()
    alfred.launch()

