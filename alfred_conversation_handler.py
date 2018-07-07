from telegram import ReplyKeyboardMarkup
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler,
                          ConversationHandler)
from alfred_user_memory import AlfredUserMemory
from alfred_news_memory import AlfredNewsMemory

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
            entry_points=[CommandHandler('personalisiere', AlfredConversationHandler.start)],

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

            fallbacks=[RegexHandler('^' + AlfredConversationHandler.option4 + '$', AlfredConversationHandler.done, pass_user_data=True)]
        )

        return conv_handler

    @staticmethod
    def start(bot, update):
        update.message.reply_text(
            "Wie soll der Filter konfiguriert werden?"
            "Bitte wählen Sie Ihre Vorlieben.",
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

        user_obj.preferences=user_data
        AlfredConversationHandler.alfred_user_memory.upsert_user(user=user_obj)

        user_data.clear()
        return ConversationHandler.END

    @staticmethod
    def facts_to_str(user_data):
        facts = list()

        for key, value in user_data.items():
            facts.append('{} - {}'.format(key, value))

        return "\n".join(facts).join(['\n', '\n'])
