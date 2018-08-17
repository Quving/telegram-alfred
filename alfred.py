#!/usr/bin/env python3

import logging
import os

from telegram.ext import Updater, CommandHandler

from alfred_exceptions import BotTokenNotSetException
from alfred_user_commands import AlfredUserCommands
from conv_handler_filter import ConvHandlerFilter
from conv_handler_menu import ConvHandlerMenu


class Alfred:
    def __init__(self):
        # Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.INFO)

        self.logger = logging.getLogger(__name__)

        token = os.getenv("ALFRED_BOT_TOKEN")
        if token is None:
            raise BotTokenNotSetException("Set the bot token.")

        self.updater = Updater(token)

        dp = self.updater.dispatcher

        # User Commands
        dp.add_handler(CommandHandler("help", AlfredUserCommands.help))
        dp.add_handler(CommandHandler("deaktivieren", AlfredUserCommands.deaktivieren))
        dp.add_handler(CommandHandler("start", AlfredUserCommands.start))
        dp.add_handler(CommandHandler("aktivieren", AlfredUserCommands.aktivieren))
        dp.add_handler(CommandHandler("weitere_nachricht", AlfredUserCommands.weitere_nachricht))

        # User Commands - Filter
        dp.add_handler(ConvHandlerFilter.conv_handler("filter"))
        dp.add_handler(ConvHandlerMenu.conv_handler("menu"))

        # Log errors.
        dp.add_error_handler(self.error)

    def error(self, bot, update, error):
        self.logger.warning('Update "%s" caused error "%s"', update, error)

    def launch(self):
        # Start the Bot.
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C.
        self.updater.idle()
