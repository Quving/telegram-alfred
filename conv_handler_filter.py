#!/usr/bin/env python3
import emoji
from telegram import ReplyKeyboardMarkup
from telegram.ext import (CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

from alfred_news_memory import AlfredNewsMemory
from alfred_user_commands import AlfredUserCommands
from alfred_user_memory import AlfredUserMemory
from helper import Helper
from user import User


class ConvHandlerFilter:
    alfred_user_memory = AlfredUserMemory()
    alfred_news_memory = AlfredNewsMemory()
    important_keys = ["region", "lokales", "rubrik"]

    CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
    option1 = emoji.emojize(':earth_africa: Region setzen', use_aliases=True)
    option2 = emoji.emojize(':mag_right: Rubrik wählen', use_aliases=True)
    option3 = emoji.emojize(':pushpin: Lokales einstellen', use_aliases=True)
    option4 = emoji.emojize(':mag: Filter anzeigen', use_aliases=True)
    option5 = emoji.emojize(':heavy_check_mark: Fertig', use_aliases=True)
    reply_keyboard = [[option1, option2], [option3, option4], [option5]]
    markup_filter = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    @staticmethod
    def conv_handler(hook):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler(hook, ConvHandlerFilter.start)],

            states={
                ConvHandlerFilter.CHOOSING: [RegexHandler('^(' + ConvHandlerFilter.option1 +
                                                          '|' + ConvHandlerFilter.option2 +
                                                          '|' + ConvHandlerFilter.option3 +
                                                          '|' + ConvHandlerFilter.option4 +
                                                          ')$',
                                                          ConvHandlerFilter.regular_choice,
                                                          pass_user_data=True),
                                             RegexHandler('^Something else...$',
                                                          ConvHandlerFilter.custom_choice),
                                             ],

                ConvHandlerFilter.TYPING_CHOICE: [MessageHandler(Filters.text,
                                                                 ConvHandlerFilter.regular_choice,
                                                                 pass_user_data=True),
                                                  ],

                ConvHandlerFilter.TYPING_REPLY: [MessageHandler(Filters.text,
                                                                ConvHandlerFilter.received_information,
                                                                pass_user_data=True),
                                                 ],
            },

            fallbacks=[RegexHandler('^' + ConvHandlerFilter.option5 + '$', ConvHandlerFilter.done,
                                    pass_user_data=True)]
        )

        return conv_handler

    @staticmethod
    def start(bot, update):
        user = update.message.from_user
        # user : {'id': 120745084, 'first_name': 'Vinh', 'is_bot': False, 'username': 'Vinguin', 'language_code': 'en-GB'}

        update.message.reply_text("\nBitte konfigurieren Sie jetzt Ihre News-Präferenzen.",
                                  reply_markup=ConvHandlerFilter.markup_filter)

        return ConvHandlerFilter.CHOOSING

    @staticmethod
    def regular_choice(bot, update, user_data):
        text = update.message.text
        user = update.message.from_user
        user_data['choice'] = ConvHandlerFilter.get_key_from_option(text)

        # Region
        if text == ConvHandlerFilter.option1:
            markup = Helper.create_replykeyboardmarkup(
                ["Hamburg", "Niedersachsen", "Mecklenburg-Vorpommern", "Schleswig-Holstein"])

        # Rubrik
        if text == ConvHandlerFilter.option2:
            markup = Helper.create_replykeyboardmarkup(["Sport", "Kultur", "Nachrichten", "Ratgeber"])

        # Lokales
        if text == ConvHandlerFilter.option3:
            key = ConvHandlerFilter.get_key_from_option(ConvHandlerFilter.option1)
            if key in user_data:
                cities = Helper.cities_from_region(user_data[key])
                markup = Helper.create_replykeyboardmarkup(cities)
            else:
                update.message.reply_markdown(
                    "Bevor Lokales eingestellt werden kann, muss die **Region** zuerst gesetzt sein.",
                    reply_markup=ConvHandlerFilter.markup_filter)
                return ConvHandlerFilter.CHOOSING

        # Filter anzeigen
        if text == ConvHandlerFilter.option4:
            user_obj = ConvHandlerFilter.alfred_user_memory.get_user_by_id(str(user["id"]))
            facts = ConvHandlerFilter.facts_to_str(user_obj.preferences)
            reply_text = "*Dein Profil:*\n\n" + facts
            update.message.reply_markdown(reply_text, reply_markup=ConvHandlerFilter.markup_filter)
            return ConvHandlerFilter.CHOOSING

        update.message.reply_markdown(
            'Bitte geben Sie ihre Wahl für *{}* an.'
                .format(ConvHandlerFilter.get_key_from_option(text).title()), reply_markup=markup)

        return ConvHandlerFilter.TYPING_REPLY

    @staticmethod
    def custom_choice(bot, update):
        update.message.reply_text('Alright, please send me the category first, '
                                  'for example "Most impressive skill"')

        return ConvHandlerFilter.TYPING_CHOICE

    @staticmethod
    def received_information(bot, update, user_data):
        text = update.message.text
        category = user_data['choice']
        user_data[category] = text.lower()
        del user_data['choice']

        update.message.reply_text("{} gespeichert.".format(
            ConvHandlerFilter.facts_to_str(user_data)), reply_markup=ConvHandlerFilter.markup_filter)

        return ConvHandlerFilter.CHOOSING

    @staticmethod
    def done(bot, update, user_data):
        if 'choice' in user_data:
            del user_data['choice']

        update.message.reply_markdown("*Folgendes Profil wurde angelegt.*\n"
                                  "{}\n\n{}".format(ConvHandlerFilter.facts_to_str(user_data),
                                                    "Geben Sie /menu ein um ins Menu zurückzukehren."))

        user = update.message.from_user
        user_id = str(user["id"])
        user_obj = ConvHandlerFilter.alfred_user_memory.get_user_by_id(user_id=user_id)

        for key in ConvHandlerFilter.important_keys:
            if key in user_data:
                data = user_data[key]
                user_obj.preferences[key] = data
        ConvHandlerFilter.alfred_user_memory.upsert_user(user=user_obj)

        user_data.clear()
        return ConversationHandler.END

    @staticmethod
    def facts_to_str(user_data):
        facts = ""
        for key, value in user_data.items():
            if key in ConvHandlerFilter.important_keys:
                if key == "region":
                    facts += ':earth_africa: ' + key.title() + ': ' + value.title() + '\n'
                elif key == "lokales":
                    facts += ':pushpin: ' + key.title() + ': ' + value.title() + '\n'
                elif key == "rubrik":
                    facts += ':mag: ' + key.title() + ': ' + value.title() + '\n'
                else:
                    pass

        return emoji.emojize(facts, use_aliases=True)

    @staticmethod
    def get_key_from_option(option):
        if option == ConvHandlerFilter.option1:
            key = "region"
        elif option == ConvHandlerFilter.option2:
            key = "rubrik"
        elif option == ConvHandlerFilter.option3:
            key = "lokales"
        elif option == ConvHandlerFilter.option4:
            key = "filter"
        else:
            key = None

        return key
