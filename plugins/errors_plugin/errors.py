# coding=utf-8
from errbot import BotPlugin, botcmd
from errbot import webhook
from flask import jsonify

import json

class Errors(BotPlugin):
    """
    Errors Reciever Plugin
    """
    # self.bot_config.CHATROOM_PRESENCE вытащить все группы
    # простая команда

    @webhook
    def errors(self, request):
        """
            {
                'nameService': 'opc-mailing',
                'error':
                    {
                        'test': 'errMessage'
                    }
            }
        """
        data = request
        print(data['error'])
        try:
            msg = f" ==>  <b>{data['nameService']}</b>"
            msg += "\n"
            msg += f"<b>ERROR</b>: {data['error']}"
        except Exception as e:
            print(e)
            msg = f"An exception occurred while trying to parse message from service"

        self.send_to_chats(msg)
        return jsonify({'status': 200})

    def send_to_chats(self, msg):
        self.send(
            self.build_identifier("-1001530829894"),
            msg
        )


