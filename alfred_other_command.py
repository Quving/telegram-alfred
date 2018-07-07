#!/usr/bin/env python3
from alfred_demo import AlfredDemo
from alfred_news_memory import AlfredNewsMemory
from alfred_user_memory import AlfredUserMemory


class AlfredOtherCommands:
    alfred_user_memory = AlfredUserMemory()
    alfred_news_memory = AlfredNewsMemory()

    @staticmethod
    def demo(bot, update):
        AlfredDemo.run(update)
