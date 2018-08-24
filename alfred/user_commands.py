#!/usr/bin/env python3
import json

from alfred.exceptions import AlfredFileWrongFormatException
from alfred.news_memory import NewsMemory
from alfred.user_memory import UserMemory
from user import User


class UserCommands:
    alfred_user_memory = UserMemory()
    alfred_news_memory = NewsMemory()

    @staticmethod
    def get_text(filename):
        with open(filename, "r") as f:
            data = json.load(f)
            if "text" not in data:
                raise AlfredFileWrongFormatException("File does not contain 'text' key.")
            return data["text"]

    @staticmethod
    def start(bot, update):
        datenschutz = UserCommands.get_text("datenschutz.json")
        user = update.message.from_user
        if not UserCommands.alfred_user_memory.user_exist_by_id(user_id_str=str(user["id"])):
            user_dict = {"id": str(user["id"]),
                         "first_name": user["first_name"],
                         "username": user["username"],
                         "preferences": {"region": "",
                                         "lokales": "",
                                         "rubrik": ""}}

            user_obj = User(user_dict=user_dict)
            UserCommands.alfred_user_memory.upsert_user(user=user_obj)
            reply_text = "Willkommen {}!\nUnter /help finden Sie alle Befehle, die Ihnen zur Verfügung stehen." \
                .format(user["first_name"])
        else:
            reply_text = "Willkommen zurück, {}!\n".format(user["first_name"])
        update.message.reply_markdown(datenschutz)
        update.message.reply_text(reply_text)

    @staticmethod
    def help(bot, update):
        help = UserCommands.get_text("help.json")
        update.message.reply_markdown(help)

    @staticmethod
    def pushoff(bot, update):
        update.message.reply_text(
            'Push Nachrichten sind deaktiviert.')

    @staticmethod
    def pushon(bot, update):
        update.message.reply_text(
            'Push Nachrichten sind aktiviert.')
