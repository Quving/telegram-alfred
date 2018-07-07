#!/usr/bin/env python3
from alfred_demo import AlfredDemo
from alfred_news_memory import AlfredNewsMemory
from alfred_user_memory import AlfredUserMemory


class AlfredOtherCommands:
    alfred_user_memory = AlfredUserMemory()
    alfred_news_memory = AlfredNewsMemory()

    @staticmethod
    def hookpoint(bot, update):
        user = update.message.from_user
        user_id = str(user["id"])

        user = AlfredOtherCommands.alfred_user_memory.get_user_by_id(user_id)
        if update.message.text == AlfredDemo.option1:
            user.preferences["clicked"] = "1"
        else:
            user.preferences["clicked"] = "0"

        AlfredOtherCommands.alfred_user_memory.upsert_user(user)

    @staticmethod
    def demo(bot, update):
        AlfredDemo.run(update)
