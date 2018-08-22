#!/usr/bin/env python3
import emoji
from telegram import ReplyKeyboardMarkup
from telegram.ext import RegexHandler, MessageHandler, ConversationHandler, Filters

from alfred_news_memory import AlfredNewsMemory
from alfred_user_memory import AlfredUserMemory
from helper import Helper


class ConvHandlerFilter:
    def __init__(self, alfred):
        self.alfred_user_memory = AlfredUserMemory()
        self.alfred_news_memory = AlfredNewsMemory()
        self.alfred = alfred
        self.important_keys = ["region", "lokales", "rubrik"]
        self.CHOOSING, self.TYPING_REPLY, self.TYPING_CHOICE = range(3)
        self.filter_option1 = emoji.emojize(':earth_africa: Region setzen', use_aliases=True)
        self.filter_option2 = emoji.emojize(':mag_right: Rubrik wählen', use_aliases=True)
        self.filter_option3 = emoji.emojize(':pushpin: Lokales einstellen', use_aliases=True)
        self.filter_option4 = emoji.emojize(':mag: Filter anzeigen', use_aliases=True)
        self.filter_option5 = emoji.emojize(':heavy_check_mark: Fertig', use_aliases=True)
        self.reply_keyboard = [[self.filter_option1, self.filter_option2],
                               [self.filter_option3, self.filter_option4],
                               [self.filter_option5]]
        self.markup_filter = ReplyKeyboardMarkup(self.reply_keyboard, one_time_keyboard=True)

        self.states = {
            self.CHOOSING: [RegexHandler('^(' + self.filter_option1 + '|' + self.filter_option2 +
                                         '|' + self.filter_option3 + '|' + self.filter_option4 + ')$',
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

        update.message.reply_text("\nBitte konfigurieren Sie jetzt Ihre News-Präferenzen.",
                                  reply_markup=self.markup_filter)

        return self.CHOOSING

    def regular_choice(self, bot, update, user_data):
        text = update.message.text
        user = update.message.from_user
        user_data['choice'] = self.get_key_from_option(text)

        # Region
        if text == self.filter_option1:
            markup = Helper.create_replykeyboardmarkup(
                ["Hamburg", "Niedersachsen", "Mecklenburg-Vorpommern", "Schleswig-Holstein"])

        # Rubrik
        if text == self.filter_option2:
            markup = Helper.create_replykeyboardmarkup(["Sport", "Kultur", "Nachrichten", "Ratgeber"])

        # Lokales
        if text == self.filter_option3:
            key = self.get_key_from_option(self.filter_option1)
            if key in user_data:
                cities = Helper.cities_from_region(user_data[key])
                markup = Helper.create_replykeyboardmarkup(cities)
            else:
                update.message.reply_markdown(
                    "Bevor Lokales eingestellt werden kann, muss die **Region** zuerst gesetzt sein.",
                    reply_markup=self.markup_filter)
                return self.CHOOSING

        # Filter anzeigen
        if text == self.filter_option4:
            user_obj = self.alfred_user_memory.get_user_by_id(str(user["id"]))
            facts = self.facts_to_str(user_obj.preferences)
            reply_text = "*Dein Profil:*\n\n" + facts
            update.message.reply_markdown(reply_text, reply_markup=self.markup_filter)
            return self.CHOOSING

        update.message.reply_markdown(
            'Bitte geben Sie ihre Wahl für *{}* an.'
                .format(self.get_key_from_option(text).title()), reply_markup=markup)

        return self.TYPING_REPLY

    def custom_choice(self, bot, update):
        update.message.reply_text('Alright, please send me the category first, '
                                  'for example "Most impressive skill"')

        return self.TYPING_CHOICE

    def received_information(self, bot, update, user_data):
        text = update.message.text
        category = user_data['choice']
        user_data[category] = text.lower()
        del user_data['choice']

        update.message.reply_text("{} gespeichert.".format(
            self.facts_to_str(user_data)), reply_markup=self.markup_filter)

        return self.CHOOSING

    def done(self, bot, update, user_data):
        if 'choice' in user_data:
            del user_data['choice']

        update.message.reply_markdown("*Folgendes Profil wurde angelegt.*\n"
                                      "{}".format(self.facts_to_str(user_data)))

        user = update.message.from_user
        user_id = str(user["id"])
        user_obj = self.alfred_user_memory.get_user_by_id(user_id=user_id)

        for key in self.important_keys:
            if key in user_data:
                data = user_data[key]
                user_obj.preferences[key] = data
        self.alfred_user_memory.upsert_user(user=user_obj)
        user_data.clear()

        # Go to Filter conv
        self.alfred.filter_conv_handler.update_state(new_state=self.alfred.menu_conv.states,
                                                     key=self.alfred.filter_conv_handler._get_key(update))
        return self.alfred.menu_conv.start(bot, update)

    def facts_to_str(self, user_data):
        facts = ""
        for key, value in user_data.items():
            if key in self.important_keys:
                if key == "region":
                    facts += ':earth_africa: ' + key.title() + ': ' + value.title() + '\n'
                elif key == "lokales":
                    facts += ':pushpin: ' + key.title() + ': ' + value.title() + '\n'
                elif key == "rubrik":
                    facts += ':mag: ' + key.title() + ': ' + value.title() + '\n'
                else:
                    pass

        return emoji.emojize(facts, use_aliases=True)

    def get_key_from_option(self, option):
        if option == self.filter_option1:
            key = "region"
        elif option == self.filter_option2:
            key = "rubrik"
        elif option == self.filter_option3:
            key = "lokales"
        elif option == self.filter_option4:
            key = "filter"
        else:
            key = None

        return key
