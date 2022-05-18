from errbot import BotPlugin, botcmd
from errbot.backends.telegram_messenger import TelegramPerson, TelegramRoom
from mongoDB import MongoDB
from xml.etree import ElementTree
import requests

from pprint import pprint


class DTN(BotPlugin):
    """
    Плагин для ДТН.
    """

    @botcmd
    def safeinfo(self, msg, args):
        """
        Safe info of the group to the mongoDB
        """
        print("to::", msg.to)
        # print("msg::", msg.to.title)
        if not hasattr(msg.to, "title"):
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
        print(query)
        # self.mongo_db.update_one('Groups', {'id': query['id']}, query, upsert=True)
        return 'Группа успешно сохранена'  # This string format is markdown.

    @botcmd
    def resendtelegram(self, msg, args):
        """
        Resend telegram msg by process instance id
        """
        def_id = self.fetch_definition_id(args)
        xml_tree = self.fetch_xml_tree(def_id)
        root = ElementTree.fromstring(xml_tree)
        tasks = self.get_all_service_tasks(root, [])
        tasks_info = self.get_task_info(tasks)
        return self.camunda_create_task(tasks_info, args)

    # функция инициализации когда плагин подключается
    # и пример отправки сообщения
    def activate(self):
        # НЕ ЗАБЫВАТЬ! ломает бота без ошибки потом не найдешь!
        super().activate()
        MongoDB.initialize(self.bot_config.MONGO_COMMERCIAL_URI, self.bot_config.MONGO_COMMERCIAL_DB_GROUP)
        self.mongo_db = MongoDB.get_db(self.bot_config.MONGO_COMMERCIAL_DB_GROUP)

    def fetch_definition_id(self, process_id):
        resp = requests.get(
            f"https://opera-bpm.bi.group/engine-rest/process-instance/{process_id}")
        resp = resp.json()
        return resp["definitionId"]

    def fetch_xml_tree(self, definition_id):
        resp = requests.get(
            f"https://opera-bpm.bi.group/engine-rest/process-definition/{definition_id}/xml")
        resp = resp.json()
        resp = list(resp.values())
        return resp[1]

    def get_all_service_tasks(self, root, tasks):
        for x in root:
            if "serviceTask" in x.tag:
                tasks.append(x)
            self.get_all_service_tasks(x, tasks)
        return tasks

    def get_task_info(self, tasks):
        info = []
        for x in tasks:
            atr = x.attrib
            for key, val in atr.items():
                if "topic" in key and val == "send-telegram":
                    info.append({
                        "id": atr["id"],
                        "name": atr["name"]
                    })

        return info

    def camunda_create_task(self, tasks_info, proc_id):
        for task_info in tasks_info:
            resp = requests.post(f"https://opera-bpm.bi.group/engine-rest/process-instance/{proc_id}/modification",
                                 json={
                                     "skipCustomListeners": True,
                                     "skipIoMappings": True,
                                     "instructions": [
                                         {
                                             "type": "startBeforeActivity",
                                             "activityId": task_info["id"]
                                         }
                                     ],
                                     "annotation": "Modified to resolve an error."
                                 })

            if resp.status_code == 204:
                return f"done for process-instance: {proc_id}, name: {task_info['name']}"
            else:
                return f"can't send for process-instance: {proc_id}, name: {task_info['name']}"
