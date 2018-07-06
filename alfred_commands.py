#!/usr/bin/env python3
from db import AlfredMemory
from user import User


class AlfredCommands:
    alfred_memory = AlfredMemory()

    @staticmethod
    def start(bot, update):
        update.message.reply_text('Hi!')
        user = update.message.from_user
        # user : {'id': 120745084, 'first_name': 'Vinh', 'is_bot': False, 'username': 'Vinguin', 'language_code': 'en-GB'}

        user_dict = {"id": str(user["id"]),
                     "first_name": user["first_name"],
                     "username": user["username"]}

        user_obj = User(user_dict=user_dict)

        AlfredCommands.alfred_memory.upsert_user(user=user_obj)

    @staticmethod
    def neues(bot, update):
        update.message.reply_text(
            'Na du, normalerweise wuerdest du jetzt Nachrichten erhalten. Aber an dieser Funktionalitaet wird noch gearbeitet. :D')

    @staticmethod
    def deaktivieren(bot, update):
        update.message.reply_text(
            'Push Nachrichten sind deaktiviert.')

    @staticmethod
    def aktivieren(bot, update):
        update.message.reply_text(
            'Push Nachrichten sind aktiviert.')

    @staticmethod
    def mehr(bot, update):
        update.message.reply_text(
            'In Bearbeitung. Weitere Informationen zum Thema X wuerden jetzt kommen.')


    @staticmethod
    def hintergrund(bot, update):
        update.message.reply_text(
            'In Bearbeitung. Mehr Hintergrund Informationen wuerden jetzt angezeigt werden.')


    @staticmethod
    def weitere_nachricht(bot, update):
        update.message.reply_text(
            'In Bearbeitung. Weitere Nachrichten wuerden hier angezeigt werden.')


    @staticmethod
    def naechste_rubrik(bot, update):
        update.message.reply_text(
            'In Bearbeitung. Die naechste Rubrik kommt. ... wenn die Funktionalitaet da ist. :)')




"""

whatsnew - Erhalte News auf Anfrage.
mute - Schalte Push Notifications aus.


"""
