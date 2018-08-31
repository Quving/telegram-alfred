#!/usr/bin/env python
# -*- coding: utf-8 -*-


class OptionCommands:

    @staticmethod
    def start(self, bot, update):
        """
        This method is the entrypoint of the conversation 'Option'.
        :param self:
        :param bot:
        :param update:
        :return:
        """
        reply_text = "Sie sind bei den Optionen. Was möchten Sie tun?"
        update.message.reply_text(reply_text,
                                  reply_markup=self.option_markup)

    @staticmethod
    def feedback(self, bot, update):
        update.message.reply_markdown("Bitte schreiben Sie nun Ihr Feedback.")

    @staticmethod
    def information(self, bot, update):
        """
        Send information about alfred.
        :param self:
        :param bot:
        :param update:
        :return:
        """
        update.message.reply_markdown("Nun werden einige Informationen zu Alfred angezeigt.",
                                      reply_markup=self.option_markup)

    @staticmethod
    def unknown(self, bot, update):
        """
        Handle unknown commands
        :param self:
        :param bot:
        :param update:
        :return:
        """
        update.message.reply_markdown(
            "Unbekannter Befehl. Bitte kontaktieren Sie das Entwicklerteam. Entschuldigung!",
            reply_markup=self.option_markup)
