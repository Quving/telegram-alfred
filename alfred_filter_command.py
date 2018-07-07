
from telegram import ReplyKeyboardMarkup

from alfred_user_memory import AlfredUserMemory
from alfred_news_memory import AlfredNewsMemory

class AlfredFilterCommands:
    alfred_user_memory = AlfredUserMemory()
    alfred_news_memory = AlfredNewsMemory()

    @staticmethod
    def setze_region(bot, update, region):
        user = update.message.from_user
        user_id = str(user["id"])

        user_obj = AlfredFilterCommands.alfred_user_memory.get_user_by_id(user_id=user_id)
        user_obj.preferences["region":region]
        print(user_obj.to_dict())
        update.message.reply_text("Erfolgreich")





