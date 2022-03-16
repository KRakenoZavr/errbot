import requests
import couchdb
from errbot import BotPlugin, botcmd
from redis import Redis
from apscheduler.schedulers.background import BackgroundScheduler
from mongoDB import MongoDB


class Pinger(BotPlugin):
    """
    Pings every server in kubernetes
    """

    # TODO adding new service with bot commands
    # @botcmd()
    # def first(self, msg, args):
    #     msg.ctx["service_name"] = "Opera Guide"
    #     return "done1"
    #
    # @botcmd()
    # def second(self, msg, args):
    #     msg.ctx["service_action"] = "request"
    #     return msg.ctx["service_name"]
    #
    # @botcmd()
    # def third(self, msg, args):
    #     return msg.ctx["service_action"]

    @botcmd()
    def remove_all_job(self):
        self.scheduler.remove_all_jobs()
        return "removed all jobs"

    def activate(self):
        super().activate()
        if not hasattr(self, "scheduler"):
            self.scheduler = BackgroundScheduler()
            self.scheduler.start()

        MongoDB.initialize(self.bot_config.MONGO_OPERA_GUIDE_URI, self.bot_config.MONGO_OPERA_GUIDE_DB_GROUP)
        self.mongo_db = MongoDB.get_db(self.bot_config.MONGO_OPERA_GUIDE_DB_GROUP)

        self.scheduler.remove_all_jobs()
        self.create_jobs(self.get_tasks_list())
        self.send_active_jobs()

    def create_jobs(self, tasks):
        for item in tasks:
            if item["action"] == "request":
                self.scheduler.add_job(self.job_type_request, 'interval', [item], minutes=5,
                                       id=item["name"])
            elif item["action"] == "redis":
                self.scheduler.add_job(self.job_type_redis, 'interval', [item], minutes=5,
                                       id=item["name"])
            elif item["action"] == "couchdb":
                self.scheduler.add_job(self.job_type_request, 'interval', [item], minutes=5,
                                       id=item["name"])

    def job_type_couchdb(self, item):
        try:
            db = couchdb.Server(item["endpoint"])
            db.version()
        except couchdb.http.Unauthorized:
            pass
        except:
            # self.warn_admins(f"Не работает сервис: {item['name']}")
            self.send_to_chats(f"Не работает сервис: {item['name']}")

    def job_type_redis(self, item):
        try:
            password = self.bot_config.__getattribute__(item["password"])
            r = Redis(host=item["host"], port=item["port"], socket_connect_timeout=1, password=password)
            r.ping()
        except:
            # self.warn_admins(f"Не работает сервис: {item['name']}")
            self.send_to_chats(f"Не работает сервис: {item['name']}")

    def job_type_request(self, item):
        try:
            r = requests.request(method="GET", url=item["endpoint"], timeout=30)
            if r.status_code >= 500:
                # self.warn_admins(f"Не работает сервис: {item['name']}")
                self.send_to_chats(f"Не работает сервис: {item['name']}")
        except:
            # self.warn_admins(f"Не работает сервис: {item['name']}")
            self.send_to_chats(f"Не работает сервис: {item['name']}")

    def send_to_chats(self, msg):
        self.send(
            self.build_identifier("-1001411828593"),
            msg
        )

    # send active jobs ids
    def send_active_jobs(self):
        job_ids = [item.id for item in self.scheduler.get_jobs()]
        job_ids = '\n'.join(job_ids)
        # self.warn_admins(f"Active pinging services: \n{job_ids}")
        self.send_to_chats(f"Active pinging services: \n{job_ids}")

    # get all tasks from mongo
    def get_tasks_list(self):
        tasks = self.mongo_db.find('activePingServices')
        tasks = list(tasks)
        return tasks
