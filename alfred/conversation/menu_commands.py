#!/usr/bin/env python
# -*- coding: utf-8 -*-


import random

from telegram import ChatAction
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from alfred.material.user import User
from alfred.user_commands import UserCommands


class MenuCommands:
    @staticmethod
    def start(self, bot, update):
        """
        That is the first method that is called for the sub conversation handler 'filter'.
        :param self:
        :param bot:
        :param update:
        :return:
        """
        user = update.message.from_user
        if not self.alfred_user_memory.user_exist_by_id(user_id_str=str(user["id"])):
            user_dict = {"id": str(user["id"]),
                         "first_name": user["first_name"],
                         "username": user["username"],
                         "preferences": {"region": "",
                                         "lokales": "",
                                         "rubrik": ""}}

            user_obj = User(user_dict=user_dict)
            UserCommands.alfred_user_memory.upsert_user(user=user_obj)
            reply_text = "Willkommen {}! Bitte ".format(user["first_name"])
        else:
            reply_text = "Sie sind im Hauptmenu. Was möchten Sie tun?"

        update.message.reply_text(reply_text,
                                  reply_markup=self.menu_markup)

    @staticmethod
    def neuigkeiten(self, bot, update):
        """
        Send news in respect to the filter that has been set by the user.
        :param self:
        :param bot:
        :param update:
        :return:
        """
        user = update.message.from_user
        user_obj = self.alfred_user_memory.get_user_by_id(str(user["id"]))
        if not "region" in user_obj.preferences or not user_obj.preferences["region"]:
            reply_text = "Es ist noch keine Region gesetzt. Bitte setzen Sie Ihren Filter in den Filter-Einstellungen."
            update.message.reply_markdown(reply_text,
                                          reply_markup=self.menu_markup)
        else:
            bot.send_chat_action(chat_id=update.message.chat_id,
                                 action=ChatAction.TYPING)
            news_list = self.ndrclient.fetch_region_news(user_obj.preferences["region"])
            if news_list:
                news = news_list[random.randint(0, len(news_list) - 1)]
                reply_text = news.to_string()

                keyboard = [[InlineKeyboardButton("Mehr zu diesem Thema",
                                                  callback_data='2'),
                             InlineKeyboardButton("Zum Volltext",
                                                  url=news.link,
                                                  callback_data='1')]]

                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_markdown(reply_text,
                                              reply_markup=reply_markup)

            else:
                reply_text = "Es gibt derzeit keine Neuigkeiten mit dem gegenwärtigen Suchfilter."

                update.message.reply_markdown(reply_text,
                                              reply_markup=self.menu_markup)

    @staticmethod
    def unknown(self, bot, update):
        """
        Handle unknown commands in this conversation.
        :param self:
        :param bot:
        :param update:
        :return:
        """
        reply_text = "Unbekannter Befehl. Bitte kontaktieren Sie das Entwicklerteam. Entschuldigung!",
        update.message.reply_markdown(reply_text,
                                      reply_markup=self.option_markup)
