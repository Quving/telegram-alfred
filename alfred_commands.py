#!/usr/bin/env python3
from db import AlfredMemory


class AlfredCommands:
    alfred_memory = AlfredMemory()

    @staticmethod
    def start(bot, update):
        update.message.reply_text('Hi!')
        user = update.message.from_user
        # user : {'id': 120745084, 'first_name': 'Vinh', 'is_bot': False, 'username': 'Vinguin', 'language_code': 'en-GB'}

        AlfredCommands.alfred_memory.upsert_user(user_id=user["id"],
                                                 data={"first_name": user["first_name"],
                                                       "username": user["username"]})

    @staticmethod
    def whats_new(bot, update):
        update.message.reply_text(
            'Na du, normalerweise wuerdest du jetzt Nachrichten erhalten. Aber an dieser Funktionalitaet wird noch gearbeitet. :D')

    @staticmethod
    def mute(bot, update):
        update.message.reply_text(
            'Ich stelle fuer dich die Push-Notifications ein.')


"""

whatsnew - Erhalte News auf Anfrage.
mute - Schalte Push Notifications aus.


"""
