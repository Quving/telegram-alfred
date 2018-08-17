#!/usr/bin/env python
# -*- coding: utf-8 -*-

from telegram import ReplyKeyboardMarkup
from telegram.ext import (CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
import random
from alfred_news_memory import AlfredNewsMemory
from alfred_user_commands import AlfredUserCommands
from alfred_user_memory import AlfredUserMemory
from user import User
import emoji
from news import NdrClient
from conv_handler_filter import ConvHandlerFilter


class ConvHandlerMenu:
    alfred_user_memory = AlfredUserMemory()
    alfred_news_memory = AlfredNewsMemory()
    ndrclient = NdrClient()
    CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
    option1 = emoji.emojize(':newspaper: News erhalten')
    option2 = emoji.emojize(':mag: Filter anzeigen', use_aliases=True)
    option3 = emoji.emojize(':wrench:Filter bearbeiten')
    option4 = emoji.emojize(':heavy_multiplication_x: Beenden')
    reply_keyboard_menu = [[option1, option2], [option3, option4]]

    markup_menu = ReplyKeyboardMarkup(reply_keyboard_menu, one_time_keyboard=True)

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    @staticmethod
    def conv_handler(hook):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler(hook, ConvHandlerMenu.start)],

            states={
                ConvHandlerMenu.CHOOSING: [RegexHandler('^(' + ConvHandlerMenu.option1 +
                                                        '|' + ConvHandlerMenu.option2 +
                                                        '|' + ConvHandlerMenu.option3 +
                                                        ')$',
                                                        ConvHandlerMenu.regular_choice,
                                                        pass_user_data=True),
                                           RegexHandler('^Something else...$',
                                                        ConvHandlerMenu.custom_choice),
                                           ],

                ConvHandlerMenu.TYPING_CHOICE: [MessageHandler(Filters.text,
                                                               ConvHandlerMenu.regular_choice,
                                                               pass_user_data=True),
                                                ],

                ConvHandlerMenu.TYPING_REPLY: [MessageHandler(Filters.text,
                                                              ConvHandlerMenu.received_information,
                                                              pass_user_data=True),
                                               ],
            },

            fallbacks=[RegexHandler('^' + ConvHandlerMenu.option4 + '$', ConvHandlerMenu.done,
                                    pass_user_data=True)]
        )

        return conv_handler

    @staticmethod
    def start(bot, update):

        user = update.message.from_user
        # user : {'id': 120745084, 'first_name': 'Vinh', 'is_bot': False, 'username': 'Vinguin', 'language_code': 'en-GB'}

        if not ConvHandlerMenu.alfred_user_memory.user_exist_by_id(user_id_str=str(user["id"])):
            user_dict = {"id": str(user["id"]),
                         "first_name": user["first_name"],
                         "username": user["username"],
                         "preferences": {"region": "", "lokales": "", "rubrik": ""}}

            user_obj = User(user_dict=user_dict)
            AlfredUserCommands.alfred_user_memory.upsert_user(user=user_obj)
            reply_text = "Willkommen" + user["first_name"] + "!"
        else:
            reply_text = "Hallo, " + user["first_name"] + "!" + "\nWas möchten Sie tun?"
        update.message.reply_text(reply_text,
                                  reply_markup=ConvHandlerMenu.markup_menu)

        return ConvHandlerMenu.CHOOSING

    @staticmethod
    def regular_choice(bot, update, user_data):
        text = update.message.text
        user = update.message.from_user
        if text == ConvHandlerMenu.option1:

            user_obj = ConvHandlerMenu.alfred_user_memory.get_user_by_id(str(user["id"]))
            if not "region" in user_obj.preferences or not user_obj.preferences["region"]:
                reply_text = "Es ist noch keine Region gesetzt. Bitte setzen Sie Ihren Filter in den Filter-Einstellungen."
            else:
                news_list = ConvHandlerMenu.ndrclient.fetch_region_news(user_obj.preferences["region"])
                news = news_list[random.randint(0, len(news_list) - 1)]
                reply_text = news.to_string()
            update.message.reply_markdown(reply_text, reply_markup=ConvHandlerMenu.markup_menu)
        if text == ConvHandlerMenu.option2:
            user_obj = ConvHandlerMenu.alfred_user_memory.get_user_by_id(str(user["id"]))
            facts = ConvHandlerMenu.facts_to_str(user_obj.preferences)
            reply_text = "*Dein Profil:*\n\n" + facts
            update.message.reply_markdown(reply_text, reply_markup=ConvHandlerMenu.markup_menu)

        if text == ConvHandlerMenu.option3:
            reply_text = "Geben Sie /filter ein um zu den Filter Einstellungen zu gelangen."
            update.message.reply_markdown(reply_text)

        return ConvHandlerMenu.CHOOSING

    @staticmethod
    def custom_choice(bot, update):
        update.message.reply_text('Alright, please send me the category first, '
                                  'for example "Most impressive skill"')

        return ConvHandlerMenu.TYPING_CHOICE

    @staticmethod
    def received_information(bot, update, user_data):
        text = update.message.text

        update.message.reply_text("Unbekannte Aktion.")

        return ConvHandlerMenu.CHOOSING

    @staticmethod
    def done(bot, update, user_data):

        update.message.reply_text("Auf Wiedersehen!")

        user = update.message.from_user
        user_id = str(user["id"])
        user_obj = ConvHandlerMenu.alfred_user_memory.get_user_by_id(user_id=user_id)

        user_obj.preferences = user_data
        ConvHandlerMenu.alfred_user_memory.upsert_user(user=user_obj)

        user_data.clear()
        return ConversationHandler.END

    @staticmethod
    def facts_to_str(user_data):
        facts = ""
        for key, value in user_data.items():
            if key in ConvHandlerFilter.important_keys:
                if key == "region":
                    facts += emoji.emojize(':earth_africa: ' + key.title() + ': ' + value.title() + '\n',
                                           use_aliases=True)
                elif key == "lokales":
                    facts += emoji.emojize(':pushpin: ' + key.title() + ': ' + value.title() + '\n',
                                           use_aliases=True)
                elif key == "rubrik":
                    facts += emoji.emojize(':mag: ' + key.title() + ': ' + value.title() + '\n',
                                           use_aliases=True)
                else:
                    pass

        return facts
