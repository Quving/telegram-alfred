class AlfredCommands:
    @staticmethod
    def start(bot, update):
        update.message.reply_text('Hi!')

    @staticmethod
    def whats_new(bot, update):
        update.message.reply_text(
            'Na du, normalerweise wuerdest du jetzt Nachrichten erhalten. Aber an dieser Funktionalitaet wird noch gearbeitet. :D')
