#!/usr/bin/env python3
import threading
import time

from telegram import ReplyKeyboardMarkup

from alfred_news_memory import AlfredNewsMemory
from alfred_user_memory import AlfredUserMemory


class AlfredDemo:
    alfred_user_memory = AlfredUserMemory()
    alfred_news_memory = AlfredNewsMemory()

    more_inf_selected = False

    text_1 = "Stromausfall: Hamburg Airport stellt den Flugbetrieb ein Der Hamburger Flughafen hat den Flugbetrieb wegen eines Stromausfalls am Sonntag eingestellt. Passagiere beklagten chaotische Zustände. Auch erste Flüge am Montag wurden bereits gestrichen. (https://www.ndr.de/nachrichten/hamburg/Stromausfall-Hamburg-Airport-stellt-Flugbetrieb-ein,flughafen1520.html)"
    text_2 = "https://www.ndr.de/fernsehen/Welche-Rechte-haben-Fluggaeste,hamj68132.html"

    option1 = "Ja, mehr Information dazu."
    option2 = "Nein, keine zusaetzlichen Informationen."

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
        update.message.reply_text(AlfredDemo.text_1 + "\nWeitere Informationen anzeigen?",
                                  reply_markup=AlfredDemo.markup)

        user = update.message.from_user
        user_id = str(user["id"])
        user_obj = AlfredDemo.alfred_user_memory.get_user_by_id(user_id)
        user_obj.preferences["clicked"] = "0"
        AlfredDemo.alfred_user_memory.upsert_user(user=user_obj)

        # Wait until button is pressed.
        timer = 15
        while timer > 0:
            timer -= 1
            time.sleep(1)
            user_obj = AlfredDemo.alfred_user_memory.get_user_by_id(user_id)

            if "clicked" in user_obj.preferences:
                if user_obj.preferences["clicked"] == "1":
                    break

        update.message.reply_text(AlfredDemo.text_2)
        update.message.reply_text("15 Sekunden")
