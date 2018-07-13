#!/usr/bin/env python3
import json

from alfred_exceptions import AlfredFileWrongFormatException
from alfred_news_memory import AlfredNewsMemory
from alfred_user_memory import AlfredUserMemory


class AlfredUserCommands:
    alfred_user_memory = AlfredUserMemory()
    alfred_news_memory = AlfredNewsMemory()

    @staticmethod
    def get_text(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            if "text" not in data:
                raise AlfredFileWrongFormatException("File does not contain 'text' key.")
            return data["text"]

    @staticmethod
    def start(bot, update):
        datenschutz = AlfredUserCommands.get_text("datenschutz.json")
        update.message.reply_text(datenschutz)

    @staticmethod
    def help(bot, update):
        help = AlfredUserCommands.get_text("help.json")
        update.message.reply_text(help)

    @staticmethod
    def neues(bot, update):
        user_tg = update.message.from_user
        user_id = str(user_tg["id"])

        user = AlfredUserCommands.alfred_user_memory.get_user_by_id(user_id)
        news_article = AlfredUserCommands.alfred_news_memory.get_neues(user.preferences)

        update.message.reply_text(news_article)

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
