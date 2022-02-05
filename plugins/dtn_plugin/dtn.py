from errbot import BotPlugin, botcmd
from errbot.backends.telegram_messenger import TelegramPerson, TelegramRoom
from mongoDB import MongoDB

class DTN(BotPlugin):
    """
    Плагин для ДТН.
    """
    @botcmd
    def safeinfo(self, msg, args):
        """
        Safe info of the group to the mongoDB
        """
        if (type(msg.to) is TelegramPerson):
            """
            Safe info works only for groups
            """
            return '/safeinfo работает только для групп'
        # res = f'id: {msg.to.id} \ntitle: {msg.to.title}'
        query = {
            'id': msg.to.id,
            'description': None,
            'title': msg.to.title,
            'type': 'supergroup'
        }
        self.mongo_db.update_one('Groups', {'id': query['id']}, query, upsert=True)
        return 'Группа успешно сохранена'  # This string format is markdown.

    # функция инициализации когда плагин подключается
    # и пример отправки сообщения
    def activate(self):
        # НЕ ЗАБЫВАТЬ! ломает бота без ошибки потом не найдешь!
        super().activate()
        MongoDB.initialize(self.bot_config.MONGO_COMMERCIAL_URI, self.bot_config.MONGO_COMMERCIAL_DB_GROUP)
        self.mongo_db = MongoDB.get_db(self.bot_config.MONGO_COMMERCIAL_DB_GROUP)
