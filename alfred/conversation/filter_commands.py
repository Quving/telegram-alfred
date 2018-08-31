#!/usr/bin/env python
# -*- coding: utf-8 -*-


from alfred.util.helper import Helper


class FilterCommands:

    @staticmethod
    def start(self, bot, update):
        """
        That is the first method that is called for the sub conversation handler 'filter'.
        :param self:
        :param bot:
        :param update:
        :return:
        """
        reply_text = "Bitte konfigurieren Sie jetzt Ihre News-Präferenzen."
        update.message.reply_text(reply_text,
                                  reply_markup=self.filter_markup)

    @staticmethod
    def region_setzen(self, bot, update):
        """
        Set a region using a pre-defined set of reply buttons.
        :param self:
        :param bot:
        :param update:
        :return:
        """
        text = update.message.text
        markup = Helper.create_replykeyboardmarkup(
            ["Hamburg", "Niedersachsen", "Mecklenburg-Vorpommern", "Schleswig-Holstein"])

        choice = self.get_key_from_option(text).title()
        update.message.reply_markdown('Bitte geben Sie ihre Wahl für *{}* an.'.format(choice),
                                      reply_markup=markup)

    @staticmethod
    def rubrik_setzen(self, bot, update):
        """
        Set a rubrik using a pre-defined set of reply buttons.
        :param self:
        :param bot:
        :param update:
        :return:
        """
        text = update.message.text
        markup = Helper.create_replykeyboardmarkup(["Sport", "Kultur", "Nachrichten", "Ratgeber"])

        choice = self.get_key_from_option(text).title()
        update.message.reply_markdown('Bitte geben Sie ihre Wahl für *{}* an.'.format(choice),
                                      reply_markup=markup)

    @staticmethod
    def lokales_setzen(self, bot, update, user_data):
        """
        Set a locales using a pre-defined set of reply buttons.
        :param self:
        :param bot:
        :param update:
        :param user_data:
        :return:
        """
        text = update.message.text
        key = self.get_key_from_option(self.filter_option1)
        if key in user_data:
            cities = Helper.cities_from_region(user_data[key])
            markup = Helper.create_replykeyboardmarkup(cities)
            choice = self.get_key_from_option(text).title()
            update.message.reply_markdown('Bitte geben Sie ihre Wahl für *{}* an.'.format(choice),
                                          reply_markup=markup)
            return self.FILTER_TYPING_REPLY
        else:
            update.message.reply_markdown(
                "Bevor Lokales eingestellt werden kann, muss die **Region** zuerst gesetzt sein.",
                reply_markup=self.filter_markup)

    @staticmethod
    def filter_anzeigen(self, bot, update):
        """
        Display the current set filter.
        :param self:
        :param bot:
        :param update:
        :return:
        """
        user = update.message.from_user
        user_obj = self.alfred_user_memory.get_user_by_id(str(user["id"]))
        facts = self.facts_to_str(user_obj.preferences)
        reply_text = "*Dein Profil:*\n\n" + facts
        update.message.reply_markdown(reply_text, reply_markup=self.filter_markup)

    @staticmethod
    def unknown(self, bot, update):
        """
        Handle unknown commands in this conversation.
        :param self:
        :param bot:
        :param update:
        :return:
        """
        update.message.reply_markdown(
            "Unbekannter Befehl. Wir bitten um Entschuldigung. Das Entwicklerteam wird sich darum kümmern.",
            reply_markup=self.filter_markup)
