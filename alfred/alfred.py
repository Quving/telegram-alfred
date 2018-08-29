#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

from telegram.ext import Updater, CommandHandler, ConversationHandler, RegexHandler
from telegram.utils.promise import Promise

from alfred import menu_conv_handler
from alfred.vars import Conts
from alfred.exceptions import AlfredConversationStorageException
from alfred.memory.conversation_memory import ConversationMemory
from alfred.user_commands import UserCommands


class Alfred:
    def __init__(self):
        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        self.logger = logging.getLogger(__name__)
        self.updater = Updater(Conts.ALFRED_BOT_TOKEN)
        self.dp = self.updater.dispatcher

        self.conversation_memory = ConversationMemory()

        self.add_commands()
        self.add_menus()

        self.load_conversations()

        self.cron = self.updater.job_queue
        job_minute = self.cron.run_repeating(callback=self.persist_conversation_states,
                                             interval=10,
                                             first=0)

    def add_commands(self):
        """
        Add commandhandlers to dispatcher.
        :return:
        """
        self.dp.add_handler(CommandHandler("help", UserCommands.help))
        self.dp.add_handler(CommandHandler("pushoff", UserCommands.pushoff))
        self.dp.add_handler(CommandHandler("pushon", UserCommands.pushon))

    def add_menus(self):
        """
        Add conversationhandler for menu to dispatchner.
        :return:
        """
        self.menu_conv = menu_conv_handler.MenuConvHandler(self)
        self.menu_conv_handler = ConversationHandler(entry_points=[CommandHandler("start", self.menu_conv.menu_start)],
                                                     states=self.menu_conv.states,
                                                     fallbacks=[RegexHandler('^' + self.menu_conv.menu_option2 + '$',
                                                                             self.menu_conv.menu_done,
                                                                             pass_user_data=True),
                                                                RegexHandler('^' + self.menu_conv.filter_option5 + '$',
                                                                             self.menu_conv.filter_done,
                                                                             pass_user_data=True)])

        self.dp.add_handler(self.menu_conv_handler)

        # Log errors.
        self.dp.add_error_handler(self.error)

    def error(self, bot, update, error):
        self.logger.warning('Update "%s" caused error "%s"', update, error)

    def load_conversations(self):
        """
        Load the stored conversation in the mongo-db to current session.
        :return:
        """
        conversations = self.conversation_memory.get_conversations()
        self.menu_conv_handler.conversations = conversations

        user_data = self.conversation_memory.get_user_datas()
        self.dp.user_data = user_data

    def persist_conversation_states(self, bot, job):
        """
        Stores the current conversation-states to mongo-db.
        :param bot:
        :param job:
        :return:
        """
        resolved = dict()
        for k, v in self.menu_conv_handler.conversations.items():
            if isinstance(v, tuple) and len(v) is 2 and isinstance(v[1], Promise):
                try:
                    new_state = v[1].result()  # Result of async function
                except:
                    new_state = v[0]  # In case async function raised an error, fallback to old state
                resolved[k] = new_state
            else:
                resolved[k] = v
        try:
            self.conversation_memory.upsert_conversation(resolved)
            self.conversation_memory.upsert_user_data(self.dp.user_data)
        except:
            raise AlfredConversationStorageException("Conversation cannot be stored.")

    def launch(self):
        # Start the Bot.
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C.
        self.updater.idle()
