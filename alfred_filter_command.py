
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

    @staticmethod
    def test(bot, update):
        CHOOSING, TYPING_REPLY, TYPING_CHOICE = range(3)

        reply_keyboard = [['Age', 'Favourite colour'],
                          ['Number of siblings', 'Something else...'],
                          ['Done']]
        markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True)

        update.message.reply_text(
            "Hi! My name is Doctor Botter. I will hold a more complex conversation with you. "
            "Why don't you tell me something about yourself?",
            reply_markup=markup)

        return CHOOSING



