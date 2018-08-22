#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

import emoji
from telegram import ReplyKeyboardMarkup
from telegram.ext import RegexHandler, MessageHandler, Filters

from alfred_news_memory import AlfredNewsMemory
from alfred_user_commands import AlfredUserCommands
from alfred_user_memory import AlfredUserMemory
from conv_handler_filter import ConvHandlerFilter
from news import NdrClient
from user import User


class ConvHandlerMenu:
    def __init__(self, alfred):
        self.alfred_user_memory = AlfredUserMemory()
        self.alfred_news_memory = AlfredNewsMemory()
        self.ndrclient = NdrClient()
        self.alfred = alfred
        self.CHOOSING, self.TYPING_REPLY, self.TYPING_CHOICE = range(3)
        self.option1 = emoji.emojize(':newspaper: News!')
        self.option2 = emoji.emojize(':mag: Mein Filter', use_aliases=True)
        self.reply_keyboard_menu = [[self.option1, self.option2]]

        self.markup_menu = ReplyKeyboardMarkup(self.reply_keyboard_menu, one_time_keyboard=True)

        self.states = {
            self.CHOOSING: [RegexHandler('^(' + self.option1 + ')$',
                                         self.regular_choice,
                                         pass_user_data=True),
                            RegexHandler('^Something else...$',
                                         self.custom_choice)],

            self.TYPING_CHOICE: [MessageHandler(Filters.text,
                                                self.regular_choice,
                                                pass_user_data=True)],

            self.TYPING_REPLY: [MessageHandler(Filters.text,
                                               self.received_information,
                                               pass_user_data=True)]}

    def start(self, bot, update):
        user = update.message.from_user
        # user : {'id': 120745084, 'first_name': 'Vinh', 'is_bot': False, 'username': 'Vinguin', 'language_code': 'en-GB'}

        if not self.alfred_user_memory.user_exist_by_id(user_id_str=str(user["id"])):
            user_dict = {"id": str(user["id"]),
                         "first_name": user["first_name"],
                         "username": user["username"],
                         "preferences": {"region": "",
                                         "lokales": "",
                                         "rubrik": ""}}

            user_obj = User(user_dict=user_dict)
            AlfredUserCommands.alfred_user_memory.upsert_user(user=user_obj)
            reply_text = "Willkommen {}! Bitte ".format(user["first_name"])
        else:
            reply_text = "Sie sind im Hauptmenu. Was möchten Sie tun?"

        update.message.reply_text(reply_text,
                                  reply_markup=self.markup_menu)

        return self.CHOOSING

    def regular_choice(self, bot, update, user_data):
        text = update.message.text
        user = update.message.from_user
        if text == self.option1:

            user_obj = self.alfred_user_memory.get_user_by_id(str(user["id"]))
            if not "region" in user_obj.preferences or not user_obj.preferences["region"]:
                reply_text = "Es ist noch keine Region gesetzt. Bitte setzen Sie Ihren Filter in den Filter-Einstellungen."
            else:
                news_list = self.ndrclient.fetch_region_news(user_obj.preferences["region"])
                if news_list:
                    news = news_list[random.randint(0, len(news_list) - 1)]
                    reply_text = news.to_string()
                else:
                    reply_text = "Es gibt derzeit keine Neuigkeiten mit dem gegenwärtigen Suchfilter."
            update.message.reply_markdown(reply_text, reply_markup=self.markup_menu)

        return self.CHOOSING

    def custom_choice(self, bot, update):
        update.message.reply_text('Alright, please send me the category first, '
                                  'for example "Most impressive skill"')

        return self.TYPING_CHOICE

    def received_information(self, bot, update, user_data):
        text = update.message.text

        update.message.reply_text("Unbekannte Aktion.")

        return self.CHOOSING

    def done(self, bot, update, user_data):
        # reply_text = "Geben Sie /filter ein um zu den Filter Einstellungen zu gelangen."
        # update.message.reply_markdown(reply_text)

        # Go to Menu conv
        self.alfred.menu_conv_handler.update_state(new_state=self.alfred.filter_conv.states,
                                                   key=self.alfred.filter_conv_handler._get_key(update))
        return self.alfred.filter_conv.start(bot, update)
