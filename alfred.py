#!/usr/bin/env python3

import logging
import os

from telegram.ext import Updater, CommandHandler

from alfred_exceptions import BotTokenNotSetException
from alfred_commands import AlfredCommands


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

        # on different commands - answer in Telegram
        dp.add_handler(CommandHandler("start", AlfredCommands.start))
        dp.add_handler(CommandHandler("help", help))
        dp.add_handler(CommandHandler("whatsnew", AlfredCommands.whats_new))
        dp.add_handler(CommandHandler("mute", AlfredCommands.mute))

        # Log errors.
        dp.add_error_handler(self.error)

    def error(self, bot, update, error):
        self.logger.warning('Update "%s" caused error "%s"', update, error)

    def launch(self):
        # Start the Bot.
        self.updater.start_polling()

        # Run the bot until you press Ctrl-C.
        self.updater.idle()
