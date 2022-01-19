from errbot import BotPlugin, botcmd, webhook


class Example(BotPlugin):
    """
    This is a very basic plugin to try out your new installation and get you started.
    Feel free to tweak me to experiment with Errbot.
    You can find me in your init directory in the subdirectory plugins.
    """
    # self.bot_config.CHATROOM_PRESENCE вытащить все группы


    # простая команда
    @botcmd
    def tryme(self, msg, args):
        """
        Execute to check if Errbot responds to command.
        Feel free to tweak me to experiment with Errbot.
        You can find me in your init directory in the subdirectory plugins.
        """
        self.warn_admins('Triggered warning')
        return "It *works* !"  # This string format is markdown.

    # будет слущать что-то вроде 1.1.1.1:3141/test
    @webhook
    def test(self, request):
        self.log.debug(repr(request))
        return "OK"

    # функция инициализации когда плагин подключается
    # и пример отправки сообщения
    def activate(self):
        # super().activate()
        self.send(
            self.build_identifier("-732525540"),
            "Plugin activated",
        )
