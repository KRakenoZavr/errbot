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
    def pinger_createpingjobs(self, msg, args):
        self.scheduler.remove_all_jobs()
        self.fetch_tasks_list()
        self.create_jobs()
        self.send_active_jobs()
        return "done"

    @botcmd()
    def pinger_removeall(self, msg, args):
        """
        remove all pinger jobs
        """
        self.scheduler.remove_all_jobs()
        return "removed all jobs"

    @botcmd()
    def pinger_pingmanually(self, msg, args):
        """
        fetch tasks from mongo then
        ping all services by bot command
        """
        self.fetch_tasks_list()
        self.run_manually_jobs()
        return "all services checked"

    def send_to_chats(self, msg):
        self.send(
            self.build_identifier("-1001411828593"),
            msg
        )

    def send_active_jobs(self):
        """
        send to telegram group active pinging services list
        """
        job_ids = [item.id for item in self.scheduler.get_jobs()]
        job_ids = '\n'.join(job_ids)
        # self.warn_admins(f"Active pinging services: \n{job_ids}")
        self.send_to_chats(f"Active pinging services: \n{job_ids}")

    def init_task_state(self):
        """
        set tasks state by name running or down
        initially set to True -> running
        """
        for task in self.tasks_list:
            self.task_state[task["name"]] = True
        print("task state:", self.task_state)

    def get_task_state(self, service_name: str) -> bool:
        """
        get task status
        :param service_name:
        :return service state
        """
        return self.task_state[service_name]

    def set_task_state(self, service_name: str, state: bool):
        """
        set task state to True -> running or False -> down
        :param service_name: name of service
        :param state: True or False
        """
        self.task_state[service_name] = state

    def fetch_tasks_list(self):
        """
        get all services to ping from mongo and save to state
        """
        tasks = self.mongo_db.find('activePingServices')
        self.tasks_list = list(tasks)
        print("pinging services list:", self.tasks_list)
        self.init_task_state()

    def reschedule_service(self, service_name, is_up):
        """
        reschedule job due to job state
        :param service_name:
        :param is_up:
        """
        job = self.scheduler.get_job(service_name)
        if is_up is True:
            job.reschedule("interval", minutes=self.DEFAULT_INTERVAL)
        else:
            job.reschedule("interval", minutes=self.IF_DOWN_INTERVAL)

    # TODO обернуть job этой функцией
    def scheduler_helper(self, service_name, state):
        """
        service state and reschedule controller
        :param service_name:
        :param state:
        """
        # service is up
        if state is True:
            # if it service was down and now running, reschedule to default interval
            if self.get_task_state(service_name) is False:
                self.reschedule_service(service_name, True)
                self.set_task_state(service_name, True)
                self.warn_admins(f"Сервис заработал: {service_name}")
        else:
            # if it service was running and now down, reschedule to down interval
            if self.get_task_state(service_name) is True:
                self.reschedule_service(service_name, False)
                self.set_task_state(service_name, False)

    def job_type_couchdb(self, item):
        try:
            username = self.bot_config.__getattribute__(item["user"])
            password = self.bot_config.__getattribute__(item["password"])
            db = couchdb.Server(item["endpoint"])
            db.login(name=username, password=password)
            db.version()
            self.scheduler_helper(item['name'], True)
        except couchdb.http.Unauthorized:
            pass
        except:
            self.scheduler_helper(item['name'], False)
            # self.warn_admins(f"Не работает сервис: {item['name']}")
            self.send_to_chats(f"Не работает сервис: {item['name']}")

    def job_type_redis(self, item):
        r = None
        try:
            password = self.bot_config.__getattribute__(item["password"])
            r = Redis(host=item["host"], port=item["port"], socket_connect_timeout=1, password=password)
            r.ping()
            self.scheduler_helper(item['name'], True)
        except:
            self.scheduler_helper(item['name'], False)
            # self.warn_admins(f"Не работает сервис: {item['name']}")
            self.send_to_chats(f"Не работает сервис: {item['name']}")
        finally:
            if r is not None:
                r.close()

    def job_type_request(self, item):
        try:
            r = requests.request(method="GET", url=item["endpoint"], timeout=30)
            if r.status_code >= 500:
                self.scheduler_helper(item['name'], False)
                # self.warn_admins(f"Не работает сервис: {item['name']}")
                self.send_to_chats(f"Не работает сервис: {item['name']}")
            else:
                self.scheduler_helper(item['name'], True)
        except:
            self.scheduler_helper(item['name'], False)
            # self.warn_admins(f"Не работает сервис: {item['name']}")
            self.send_to_chats(f"Не работает сервис: {item['name']}")

    # TODO make both func normal
    def run_manually_jobs(self):
        for item in self.tasks_list:
            if item["action"] == "request":
                self.job_type_request(item)
            elif item["action"] == "redis":
                self.job_type_redis(item)
            elif item["action"] == "couchdb":
                self.job_type_couchdb(item)

    def create_jobs(self):
        for item in self.tasks_list:
            if item["action"] == "request":
                self.scheduler.add_job(self.job_type_request, 'interval', [item], minutes=self.DEFAULT_INTERVAL,
                                       id=item["name"])
            elif item["action"] == "redis":
                self.scheduler.add_job(self.job_type_redis, 'interval', [item], minutes=self.DEFAULT_INTERVAL,
                                       id=item["name"])
            elif item["action"] == "couchdb":
                self.scheduler.add_job(self.job_type_couchdb, 'interval', [item], minutes=self.DEFAULT_INTERVAL,
                                       id=item["name"])

    def activate(self):
        super().activate()
        self.task_state = {}
        self.DEFAULT_INTERVAL = 5
        self.IF_DOWN_INTERVAL = 1
        if not hasattr(self, "scheduler"):
            self.scheduler = BackgroundScheduler()
            self.scheduler.start()

        MongoDB.initialize(self.bot_config.MONGO_OPERA_GUIDE_URI, self.bot_config.MONGO_OPERA_GUIDE_DB_GROUP)
        self.mongo_db = MongoDB.get_db(self.bot_config.MONGO_OPERA_GUIDE_DB_GROUP)

        self.scheduler.remove_all_jobs()
        self.fetch_tasks_list()
        self.create_jobs()
        self.send_active_jobs()
