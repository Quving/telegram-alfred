#!/usr/bin/env python3

import logging
import os

from telegram.ext import Updater, CommandHandler, ConversationHandler, RegexHandler

import conv_handler_menu
from alfred_exceptions import BotTokenNotSetException
from alfred_user_commands import AlfredUserCommands


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

		self.dp = self.updater.dispatcher

	def add_commands(self):
		# User Commands
		self.dp.add_handler(CommandHandler("help", AlfredUserCommands.help))
		self.dp.add_handler(CommandHandler("pushoff", AlfredUserCommands.pushoff))
		self.dp.add_handler(CommandHandler("start", AlfredUserCommands.start))
		self.dp.add_handler(CommandHandler("pushon", AlfredUserCommands.pushon))

	def add_menus(self):
		# ConversationHandler for Menu
		self.menu_conv = conv_handler_menu.ConvHandlerMenu(self)
		self.menu_conv_handler = ConversationHandler(entry_points=[CommandHandler("menu", self.menu_conv.menu_start)],
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

	def launch(self):
		# Start the Bot.
		self.updater.start_polling()

		# Run the bot until you press Ctrl-C.
		self.updater.idle()
