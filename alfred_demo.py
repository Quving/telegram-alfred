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
    text_3 = "Wenn der Strom - wie in dieser Woche im Norden der Stadt - für wenige Sekunden weg ist, dann ist das eine eindrucksvolle Erinnerung daran, dass ohne Elektrizität nichts mehr geht. Was ein Stromausfall anrichten kann, das hat man kürzlich am Hamburger Flughafen erlebt. Vielleicht sind solche Vorfälle von Zeit zu Zeit sogar ganz heilsam, meint NDR 90,3-Chef Hendrik Lünenborg in seinem Kommentar.\n\nhttps://www.ndr.de/nachrichten/hamburg/Kommentar-Investitionen-in-Stromnetze-wichtig,hamburgkommentar256.html"

    option1 = "Ja, mehr Information dazu."
    option2 = "Nein, keine zusaetzlichen Informationen."

    option3 = "Ja, Ich moechte auf den Laufenden gehalten werden."
    option4 = "Nein, Ich bin an diesem Thema nicht mehr interessiert."
    reply_keyboard_1 = [[option1, option2]]
    reply_keyboard_2 = [[option3, option4]]

    markup1 = ReplyKeyboardMarkup(reply_keyboard_1, one_time_keyboard=True)
    markup2 = ReplyKeyboardMarkup(reply_keyboard_2, one_time_keyboard=True)

    @staticmethod
    def run(update):
        thread = threading.Thread(target=AlfredDemo.perform, args=[update])
        thread.start()

    @staticmethod
    def perform(update):
        AlfredDemo.more_inf_selected = False
        time.sleep(3)
        update.message.reply_text(AlfredDemo.text_1)

        update.message.reply_text("\nWeitere Informationen anzeigen?",
                                  reply_markup=AlfredDemo.markup1)

        user = update.message.from_user
        user_id = str(user["id"])
        user_obj = AlfredDemo.alfred_user_memory.get_user_by_id(user_id)
        user_obj.preferences["clicked"] = "0"
        AlfredDemo.alfred_user_memory.upsert_user(user=user_obj)

        # Wait until button is pressed.
        timer = 300
        while timer > 0:
            timer -= 1
            time.sleep(1)
            user_obj = AlfredDemo.alfred_user_memory.get_user_by_id(user_id)

            if "clicked" in user_obj.preferences:
                if user_obj.preferences["clicked"] == "1":
                    break

        if user_obj.preferences["clicked"] == "1":
            update.message.reply_text(AlfredDemo.text_2)
            update.message.reply_text("15 Sekunden")

            time.sleep(3)

            update.message.reply_text(AlfredDemo.text_3)


            time.sleep(2)
            update.message.reply_text("Wie moechten Sie fortfahren?",
                                      reply_markup=AlfredDemo.markup2)
