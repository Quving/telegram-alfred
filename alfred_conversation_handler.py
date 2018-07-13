#!/usr/bin/env python3
from telegram import ReplyKeyboardMarkup
from telegram.ext import (CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)

from alfred_news_memory import AlfredNewsMemory
from alfred_user_commands import AlfredUserCommands
from alfred_user_memory import AlfredUserMemory
from user import User


class AlfredConversationHandler:
    alfred_user_memory = AlfredUserMemory()
    alfred_news_memory = AlfredNewsMemory()

    CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)
    option1 = 'Region'
    option2 = 'Rubrik'
    option3 = 'Lokales'
    option4 = 'Fertig'
    reply_keyboard = [[option1, option2], [option3, option4]]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    @staticmethod
    def get_conversation_hander():
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', AlfredConversationHandler.start)],

            states={
                AlfredConversationHandler.CHOOSING: [RegexHandler('^(' + AlfredConversationHandler.option1 +
                                                                  '|' + AlfredConversationHandler.option2 +
                                                                  '|' + AlfredConversationHandler.option3 +
                                                                  ')$',
                                                                  AlfredConversationHandler.regular_choice,
                                                                  pass_user_data=True),
                                                     RegexHandler('^Something else...$',
                                                                  AlfredConversationHandler.custom_choice),
                                                     ],

                AlfredConversationHandler.TYPING_CHOICE: [MessageHandler(Filters.text,
                                                                         AlfredConversationHandler.regular_choice,
                                                                         pass_user_data=True),
                                                          ],

                AlfredConversationHandler.TYPING_REPLY: [MessageHandler(Filters.text,
                                                                        AlfredConversationHandler.received_information,
                                                                        pass_user_data=True),
                                                         ],
            },

            fallbacks=[RegexHandler('^' + AlfredConversationHandler.option4 + '$', AlfredConversationHandler.done,
                                    pass_user_data=True)]
        )

        return conv_handler

    @staticmethod
    def start(bot, update):

        user = update.message.from_user
        # user : {'id': 120745084, 'first_name': 'Vinh', 'is_bot': False, 'username': 'Vinguin', 'language_code': 'en-GB'}

        user_dict = {"id": str(user["id"]),
                     "first_name": user["first_name"],
                     "username": user["username"]}

        user_obj = User(user_dict=user_dict)
        AlfredUserCommands.alfred_user_memory.upsert_user(user=user_obj)
        update.message.reply_text("Moin, " +
                                  user["first_name"] + "!" +
                                  "\nDarf ich mich vorstellen: Ich bin Alfred, ihr News-Bot’ler!"
                                  "\nBitte konfigurieren Sie jetzt Ihre News-Präferenzen.",
                                  reply_markup=AlfredConversationHandler.markup)

        return AlfredConversationHandler.CHOOSING

    @staticmethod
    def regular_choice(bot, update, user_data):
        text = update.message.text
        user_data['choice'] = text.lower()
        update.message.reply_text(
            'Bitte geben Sie ihre Wahl für {} an.'.format(text))

        return AlfredConversationHandler.TYPING_REPLY

    @staticmethod
    def custom_choice(bot, update):
        update.message.reply_text('Alright, please send me the category first, '
                                  'for example "Most impressive skill"')

        return AlfredConversationHandler.TYPING_CHOICE

    @staticmethod
    def received_information(bot, update, user_data):
        text = update.message.text
        category = user_data['choice']
        user_data[category] = text.lower()
        del user_data['choice']

        update.message.reply_text("{} gespeichert.".format(
            AlfredConversationHandler.facts_to_str(user_data)), reply_markup=AlfredConversationHandler.markup)

        return AlfredConversationHandler.CHOOSING

    @staticmethod
    def done(bot, update, user_data):
        if 'choice' in user_data:
            del user_data['choice']

        update.message.reply_text("Folgendes Profil wurde angelegt."
                                  "{}".format(AlfredConversationHandler.facts_to_str(user_data)))

        user = update.message.from_user
        user_id = str(user["id"])
        user_obj = AlfredConversationHandler.alfred_user_memory.get_user_by_id(user_id=user_id)

        user_obj.preferences = user_data
        AlfredConversationHandler.alfred_user_memory.upsert_user(user=user_obj)

        user_data.clear()
        return ConversationHandler.END

    @staticmethod
    def facts_to_str(user_data):
        facts = list()

        for key, value in user_data.items():
            facts.append('{} - {}'.format(key, value))

        return "\n".join(facts).join(['\n', '\n'])
