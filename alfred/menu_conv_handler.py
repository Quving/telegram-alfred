#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random

from telegram import ReplyKeyboardMarkup
from telegram.ext import RegexHandler, MessageHandler, Filters

from alfred.material.news import NdrClient
from alfred.material.user import User
from alfred.memory.news_memory import NewsMemory
from alfred.memory.user_memory import UserMemory
from alfred.user_commands import UserCommands
from alfred.util.helper import Helper


class MenuConvHandler:
	def __init__(self, alfred):
		# Memories
		self.alfred_user_memory = UserMemory()
		self.alfred_news_memory = NewsMemory()

		self.ndrclient = NdrClient()
		self.alfred = alfred

		self.menu_set = False
		self.filter_set = False

		self.init_menu()
		self.init_filter()

		self.init_conv_handler()

	def init_conv_handler(self):
		if self.filter_set and self.menu_set:
			self.states = {**self.menu_states, **self.filter_states}

	def init_menu(self):
		"""
		Initiliaze Menu-contents
		:return:
		"""
		self.MENU_CHOOSING, self.MENUTYPING_REPLY, self.MENU_TYPING_CHOICE, \
		self.FILTER_CHOOSING, self.FILTERTYPING_REPLY, self.FILTER_TYPING_CHOICE = range(6)

		# Menu Elements
		self.menu_option1 = Helper.to_emoji_str(':newspaper: Was gibt\'s Neues?')
		self.menu_option2 = Helper.to_emoji_str(':mag: Mein Filter')
		self.menu_option3 = Helper.to_emoji_str(':bell: Hilfe anzeigen')
		self.menu_option4 = Helper.to_emoji_str(':arrow_right_hook: Andere Optionen')
		self.menu_reply_keyboard = [[self.menu_option1, self.menu_option2],
		                            [self.menu_option3, self.menu_option4]]
		self.menu_markup = ReplyKeyboardMarkup(self.menu_reply_keyboard, one_time_keyboard=False)

		self.menu_states = {
			self.MENU_CHOOSING: [
				RegexHandler("^({}|{}|{})$".format(self.menu_option1,
				                                   self.menu_option3,
				                                   self.menu_option4),
				             self.menu_regular_choice,
				             pass_user_data=True)],
			self.MENU_TYPING_CHOICE: [MessageHandler(Filters.text,
			                                         self.menu_regular_choice,
			                                         pass_user_data=True)],

			self.MENUTYPING_REPLY: [MessageHandler(Filters.text,
			                                       self.menu_received_information,
			                                       pass_user_data=True)]
		}

		self.menu_set = True

	def init_filter(self):
		"""
		Initiliaze Menu-contents
		:return:
		"""
		# Filter Elements
		self.important_keys = ["region", "lokales", "rubrik"]
		self.filter_option1 = Helper.to_emoji_str(':earth_africa: Region setzen')
		self.filter_option2 = Helper.to_emoji_str(':mag_right: Rubrik wählen')
		self.filter_option3 = Helper.to_emoji_str(':pushpin: Lokales einstellen')
		self.filter_option4 = Helper.to_emoji_str(':mag: Filter anzeigen')
		self.filter_option5 = Helper.to_emoji_str(':heavy_check_mark: Fertig')
		self.filter_reply_keyboard = [[self.filter_option1, self.filter_option2],
		                              [self.filter_option3, self.filter_option4], [self.filter_option5]]
		self.filter_markup = ReplyKeyboardMarkup(self.filter_reply_keyboard, one_time_keyboard=False)

		self.filter_states = {
			self.FILTER_CHOOSING: [RegexHandler("^({}|{}|{})$".format(self.filter_option1,
			                                                          self.filter_option2,
			                                                          self.filter_option3),
			                                    self.filter_regular_choice, pass_user_data=True)],

			self.FILTER_TYPING_CHOICE: [MessageHandler(Filters.text, self.filter_regular_choice, pass_user_data=True)],

			self.FILTERTYPING_REPLY: [
				MessageHandler(Filters.text, self.filter_received_information, pass_user_data=True)]
		}
		self.filter_set = True

	def menu_start(self, bot, update):
		"""
		Menu entrypoint.
		:param bot:
		:param update:
		:return:
		"""
		user = update.message.from_user

		# Welcome-text
		UserCommands.start(bot, update)

		if not self.alfred_user_memory.user_exist_by_id(user_id_str=str(user["id"])):
			user_dict = {"id": str(user["id"]),
			             "first_name": user["first_name"],
			             "username": user["username"],
			             "preferences": {"region": "",
			                             "lokales": "",
			                             "rubrik": ""}}

			user_obj = User(user_dict=user_dict)
			UserCommands.alfred_user_memory.upsert_user(user=user_obj)
			reply_text = "Willkommen {}! Bitte ".format(user["first_name"])
		else:
			reply_text = "Sie sind im Hauptmenu. Was möchten Sie tun?"

		update.message.reply_text(reply_text,
		                          reply_markup=self.menu_markup)

		return self.MENU_CHOOSING

	def menu_regular_choice(self, bot, update, user_data):
		"""
		Handles options chosen in menu.
		:param bot:
		:param update:
		:param user_data:
		:return:
		"""
		text = update.message.text
		user = update.message.from_user

		reply_text = ""
		if text == self.menu_option1:
			user_obj = self.alfred_user_memory.get_user_by_id(str(user["id"]))
			if not "region" in user_obj.preferences or not user_obj.preferences["region"]:
				reply_text = "Es ist noch keine Region gesetzt. Bitte setzen Sie Ihren Filter in den Filter-Einstellungen."
			else:
				news_list = self.ndrclient.fetch_region_news(user_obj.preferences["region"])
				if news_list:
					news = news_list[random.randint(0, len(news_list) - 1)]
					reply_text = news.to_string()
				else:
					reply_text = "Es gibt derzeit keine Neuigkeiten mit dem gegenwärtigen Suchfilter."

				update.message.reply_markdown(reply_text,
				                              reply_markup=self.menu_markup)

		elif text == self.menu_option3:
			UserCommands.help(bot, update)

		elif text == self.menu_option4:
			UserCommands.help(bot, update)

		else:
			reply_text = "Unbekannter Befehl."
			update.message.reply_markdown(reply_text, reply_markup=self.menu_markup)

		return self.MENU_CHOOSING

	def menu_received_information(self, bot, update, user_data):
		update.message.reply_text("Unbekannte Aktion.")

		return self.MENU_CHOOSING

	def menu_done(self, bot, update, user_data):
		"""
		Switch to Filter.
		:param bot:
		:param update:
		:param user_data:
		:return:
		"""
		return self.filter_start(bot, update)

	def filter_start(self, bot, update):
		"""
		Entrypoint for filter-menu
		:param bot:
		:param update:
		:return:
		"""
		reply_text = "Bitte konfigurieren Sie jetzt Ihre News-Präferenzen."
		update.message.reply_text(reply_text,
		                          reply_markup=self.filter_markup)

		return self.FILTER_CHOOSING

	def filter_regular_choice(self, bot, update, user_data):
		"""
		Handles chosen option in filter-menu.
		:param bot:
		:param update:
		:param user_data:
		:return:
		"""
		text = update.message.text
		user_data['choice'] = self.get_key_from_option(text)

		# Region
		if text == self.filter_option1:
			markup = Helper.create_replykeyboardmarkup(
				["Hamburg", "Niedersachsen", "Mecklenburg-Vorpommern", "Schleswig-Holstein"])

		# Rubrik
		elif text == self.filter_option2:
			markup = Helper.create_replykeyboardmarkup(["Sport", "Kultur", "Nachrichten", "Ratgeber"])

		# Lokales
		elif text == self.filter_option3:
			key = self.get_key_from_option(self.filter_option1)
			if key in user_data:
				cities = Helper.cities_from_region(user_data[key])
				markup = Helper.create_replykeyboardmarkup(cities)
			else:
				update.message.reply_markdown(
					"Bevor Lokales eingestellt werden kann, muss die **Region** zuerst gesetzt sein.",
					reply_markup=self.filter_markup)
				return self.FILTER_CHOOSING

		# Filter anzeigen
		elif text == self.filter_option4:
			user = update.message.from_user
			user_obj = self.alfred_user_memory.get_user_by_id(str(user["id"]))
			facts = self.facts_to_str(user_obj.preferences)
			reply_text = "*Dein Profil:*\n\n" + facts
			update.message.reply_markdown(reply_text, reply_markup=self.filter_markup)
			return self.FILTER_CHOOSING

		else:
			update.message.reply_markdown(
				"Unbekannter Befehl",
				reply_markup=self.filter_markup)

			return self.FILTER_CHOOSING
		update.message.reply_markdown(
			'Bitte geben Sie ihre Wahl für *{}* an.'.format(self.get_key_from_option(text).title()),
			reply_markup=markup)

		return self.FILTERTYPING_REPLY

	def filter_received_information(self, bot, update, user_data):
		"""
		Handles user choice.
		:param bot:
		:param update:
		:param user_data:
		:return:
		"""
		text = update.message.text
		category = user_data['choice']
		user_data[category] = text.lower()
		del user_data['choice']

		update.message.reply_text("{} gespeichert.".format(
			self.facts_to_str(user_data)), reply_markup=self.filter_markup)

		return self.FILTER_CHOOSING

	def filter_done(self, bot, update, user_data):
		"""
		Finish filter-menu.
		:param bot:
		:param update:
		:param user_data:
		:return:
		"""
		if 'choice' in user_data:
			del user_data['choice']

		reply_text = "An Ihrem Profil hat sich nichts geändert."
		if self.facts_to_str(user_data):
			reply_text = "*Folgendes Profil wurde angelegt.*\n{}".format(self.facts_to_str(user_data))

		update.message.reply_markdown(reply_text)

		user = update.message.from_user
		user_id = str(user["id"])
		user_obj = self.alfred_user_memory.get_user_by_id(user_id=user_id)

		for key in self.important_keys:
			if key in user_data:
				data = user_data[key]
				user_obj.preferences[key] = data
		self.alfred_user_memory.upsert_user(user=user_obj)
		user_data.clear()

		return self.menu_start(bot, update)

	def init_option(self):
		"""
		Initiliaze Option-contents
		:return:
		"""
		# Option Elements
		self.important_keys = ["region", "lokales", "rubrik"]
		self.option_option1 = Helper.to_emoji_str(':speech_balloon: Feedback geben')
		self.option_option2 = Helper.to_emoji_str(':open_file_folder: Datenschutz lesen')
		self.option_option3 = Helper.to_emoji_str(':busts_in_silhouette: Informationen zu Alfred erhalten')
		self.option_option5 = Helper.to_emoji_str(':arrow_right_hook: Zum Menu')
		self.option_reply_keyboard = [[self.filter_option1, self.filter_option2],
		                              [self.filter_option3, self.filter_option4], [self.filter_option5]]
		self.filter_markup = ReplyKeyboardMarkup(self.filter_reply_keyboard, one_time_keyboard=False)

		self.option_states = {
			self.OPTION_CHOOSING: [RegexHandler("^({}|{}|{})$".format(self.option_option1,
			                                                          self.option_option2,
			                                                          self.option_option3,
			                                                          self.option_option4),
			                                    self.filter_regular_choice, pass_user_data=True)],

			self.OPTION_TYPING_CHOICE: [MessageHandler(Filters.text, self.filter_regular_choice, pass_user_data=True)],

			self.OPTION_TYPING_REPLY: [
				MessageHandler(Filters.text, self.filter_received_information, pass_user_data=True)]

		}

	def option_start(self, bot, update):
		"""
		Entrypoint for filter-menu
		:param bot:
		:param update:
		:return:
		"""
		reply_text = "Sie sind bei den Optionen. Was möchten Sie tun?"
		update.message.reply_text(reply_text,
		                          reply_markup=self.option_markup)

		return self.OPTION_CHOOSING

	def option_regular_choice(self, bot, update, user_data):
		"""
		Handles chosen option in filter-menu.
		:param bot:
		:param update:
		:param user_data:
		:return:
		"""
		text = update.message.text
		user_data['choice'] = self.get_key_from_option(text)

		# Feedback
		if text == self.option_option1:
			UserCommands.get_datenschutz(bot, update)
			return self.
		# Datenschutz
		if text == self.option_option2:
			markup = Helper.create_replykeyboardmarkup(["Sport", "Kultur", "Nachrichten", "Ratgeber"])

		# Informationen zu Alfred?
		if text == self.option_option3:
			key = self.get_key_from_option(self.option_option1)
			if key in user_data:
				cities = Helper.cities_from_region(user_data[key])
				markup = Helper.create_replykeyboardmarkup(cities)
			else:
				update.message.reply_markdown(
					"Bevor Lokales eingestellt werden kann, muss die **Region** zuerst gesetzt sein.",
					reply_markup=self.option_markup)
				return self.FILTER_CHOOSING

		# Zum Menu
		if text == self.option_option4:
			user = update.message.from_user
			user_obj = self.alfred_user_memory.get_user_by_id(str(user["id"]))
			facts = self.facts_to_str(user_obj.preferences)
			reply_text = "*Dein Profil:*\n\n" + facts
			update.message.reply_markdown(reply_text, reply_markup=self.option_markup)
			return self.OPTION_CHOOSING

		update.message.reply_markdown(
			'Bitte geben Sie ihre Wahl für *{}* an.'
				.format(self.get_key_from_option(text).title()), reply_markup=markup)

		return self.OPTION_TYPING_REPLY

	def option_received_information(self, bot, update, user_data):
		"""
		Handles user choice.
		:param bot:
		:param update:
		:param user_data:
		:return:
		"""
		text = update.message.text
		category = user_data['choice']
		user_data[category] = text.lower()
		del user_data['choice']

		update.message.reply_text("{} gespeichert.".format(
			self.facts_to_str(user_data)), reply_markup=self.option_markup)

		return self.OPTION_CHOOSING

	def option_done(self, bot, update, user_data):
		"""
		Finish filter-menu.
		:param bot:
		:param update:
		:param user_data:
		:return:
		"""
		if 'choice' in user_data:
			del user_data['choice']

		reply_text = "An Ihrem Profil hat sich nichts geändert."
		if self.facts_to_str(user_data):
			reply_text = "*Folgendes Profil wurde angelegt.*\n{}".format(self.facts_to_str(user_data))

		update.message.reply_markdown(reply_text)

		user = update.message.from_user
		user_id = str(user["id"])
		user_obj = self.alfred_user_memory.get_user_by_id(user_id=user_id)

		for key in self.important_keys:
			if key in user_data:
				data = user_data[key]
				user_obj.preferences[key] = data
		self.alfred_user_memory.upsert_user(user=user_obj)
		user_data.clear()

		return self.menu_start(bot, update)

	def facts_to_str(self, user_data):
		"""
		Summerizes the current user selection to printable text.
		:param user_data:
		:return:
		"""
		facts = ""
		for key, value in user_data.items():
			if key in self.important_keys:
				if key == "region":
					facts += ':earth_africa: {}: {}\n'.format(key.title(), value.title())
				elif key == "lokales":
					facts += ':pushpin: {}: {}\n'.format(key.title(), value.title())
				elif key == "rubrik":
					facts += ':mag: {}: {}\n'.format(key.title(), value.title())

		return Helper.to_emoji_str(facts)

	def get_key_from_option(self, option):
		if option == self.filter_option1:
			key = "region"
		elif option == self.filter_option2:
			key = "rubrik"
		elif option == self.filter_option3:
			key = "lokales"
		elif option == self.filter_option4:
			key = "filter"
		else:
			key = None

		return key
