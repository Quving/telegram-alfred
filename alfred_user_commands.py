#!/usr/bin/env python3
import json

from alfred_exceptions import AlfredFileWrongFormatException
from alfred_news_memory import AlfredNewsMemory
from alfred_user_memory import AlfredUserMemory
from user import User


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
        user = update.message.from_user
        if not AlfredUserCommands.alfred_user_memory.user_exist_by_id(user_id_str=str(user["id"])):
            user_dict = {"id": str(user["id"]),
                         "first_name": user["first_name"],
                         "username": user["username"],
                         "preferences": {"region": "",
                                         "lokales": "",
                                         "rubrik": ""}}

            user_obj = User(user_dict=user_dict)
            AlfredUserCommands.alfred_user_memory.upsert_user(user=user_obj)
            reply_text = "Willkommen {}!\nUnter /help finden Sie alle Befehle, die Ihnen zur Verfügung stehen." \
                .format(user["first_name"])
        else:
            reply_text = "Willkommen zurück, {}!\n".format(user["first_name"])
        update.message.reply_markdown(datenschutz)
        update.message.reply_text(reply_text)

    @staticmethod
    def help(bot, update):
        help = AlfredUserCommands.get_text("help.json")
        update.message.reply_markdown(help)

    @staticmethod
    def pushoff(bot, update):
        update.message.reply_text(
            'Push Nachrichten sind deaktiviert.')

    @staticmethod
    def pushon(bot, update):
        update.message.reply_text(
            'Push Nachrichten sind aktiviert.')
