#!/usr/bin/env python3
import threading
import time

from telegram import ReplyKeyboardMarkup


class AlfredDemo:
    more_inf_selected = False

    text_1 = "Stromausfall: Hamburg Airport stellt den Flugbetrieb ein Der Hamburger Flughafen hat den Flugbetrieb wegen eines Stromausfalls am Sonntag eingestellt. Passagiere beklagten chaotische Zustände. Auch erste Flüge am Montag wurden bereits gestrichen. (https://www.ndr.de/nachrichten/hamburg/Stromausfall-Hamburg-Airport-stellt-Flugbetrieb-ein,flughafen1520.html)"
    text_2 = "https://www.ndr.de/fernsehen/Welche-Rechte-haben-Fluggaeste,hamj68132.html"

    option1 = "Ja"
    option2 = "Nein"
    reply_keyboard = [[option1, option2]]

    markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

    @staticmethod
    def run(update):
        thread = threading.Thread(target=AlfredDemo.perform, args=[update])
        thread.start()

    @staticmethod
    def perform(update):
        AlfredDemo.more_inf_selected = False
        time.sleep(3)
        update.message.reply_text(AlfredDemo.text_1)

        update.message.reply_text("Weitere Informationen anzeigen?",
            reply_markup=AlfredDemo.markup)

        user = update.message.from_user
        user_id = str(user["id"])



        # Wait until button is pressed.
        while not AlfredDemo.more_inf_selected:
            time.sleep(1)

            text = update.message.text

        print("Hal")
        update.message.reply_text(AlfredDemo.text_2)

        update.message.reply_text("15 Sekunden")
