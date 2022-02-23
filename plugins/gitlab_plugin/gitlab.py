from errbot import BotPlugin, botcmd
from errbot import webhook
from flask import jsonify

import json

class Gitlab(BotPlugin):
    """
    Gitlab Webhook Reciever
    """
    # self.bot_config.CHATROOM_PRESENCE вытащить все группы
    # простая команда

    # будет слущать что-то вроде 1.1.1.1:3141/test
    @webhook
    def gitlab(self, request):

        data = request
        # json contains an attribute that differenciates between the types, see
        # https://docs.gitlab.com/ce/user/project/integrations/webhooks.html
        # for more infos
        kind = data['object_kind']
        self.log.info(f"Message Kind: {kind}")
        if kind == 'push':
            msg = generatePushMsg(data)
            self.send_to_chats(msg)
        elif kind == 'merge_request':
            msg = generateMergeRequestMsg(data)
            self.send_to_chats(msg)
        return jsonify({'status': 'ok'})

    def send_to_chats(self, msg):
        self.send(
            self.build_identifier("-1001411828593"),
            # self.build_identifier("-1001691601943"),
            msg
        )


def generatePushMsg(data):
    user = data["user_username"]
    project = data["project"]
    msg = f'<i><b>{user}</b></i> '
    msg += f'<a href="{project["web_url"]}/compare/{data["before"]}...{data["after"]}">pushed</a> '
    msg += f'to <u><a href="{project["web_url"]}">{project["name"]}</a></u>:'
    msg += "\n"
    modified_files = dict()
    added_files = dict()
    removed_files = dict()
    if len(data["commits"]):
        for commit in data["commits"]:
            for file in commit["added"]:
                added_files[file] = 1
            for file in commit["modified"]:
                modified_files[file] = 1
            for file in commit["removed"]:
                removed_files[file] = 1
        for commit in data["commits"][:2]:
            msg += f'{commit["author"]["name"]}: '
            msg += f'<a href="{commit["url"]}">'

            msg += f"{commit['title']}"
            msg += "</a>"
            msg += "\n"
        if len(data["commits"]) > 2:
            msg += "... else "
            msg += f'<a href="{project["web_url"]}/compare/{data["before"]}...{data["after"]}">{len(data["commits"])-2} '
            if (len(data["commits"])-2) > 1:
                msg += "commits</a>"
            else:
                msg += "commit</a>"
        else:
            msg += "\n"
            msg += f'<a href="{project["web_url"]}/compare/{data["before"]}...{data["after"]}">{len(data["commits"])} '
            if len(data["commits"]) > 1:
                msg += "commits</a>"
            else:
                msg += "commit</a>"
    else:
        msg += "<b>0 commits<\b>"

    msg += "\n"
    info_added = False
    if len(modified_files.keys()):
        msg += f'<b>{len(modified_files.keys())}</b> '
        if not info_added:
            if len(modified_files.keys()) > 1:
                msg += "files "
            else:
                msg += "file "
        msg += "modified "
        info_added = True
    if len(added_files.keys()):
        msg += f'<b>{len(added_files.keys())}</b> '
        if not info_added:
            if len(added_files.keys()) > 1:
                msg += "files "
            else:
                msg += "file "
        msg += "added "
        info_added = True
    if len(removed_files.keys()):
        msg += f'<b>{len(removed_files.keys())}</b> '
        if not info_added:
            if len(removed_files.keys()) > 1:
                msg += "files "
            else:
                msg += "file "
        msg += "removed"
    return msg

def generateMergeRequestMsg(data):
    user = data["user"]
    project = data["project"]
    msg = ""

    oa = data["object_attributes"]
    key = "action"
    if key not in oa:
        key = "state"
    if oa[key] == "open" or oa[key] == "reopen":
        msg += f'<i><b>{user["username"]}</b></i> '
        msg += f'{oa[key]}ed '
        msg += f'<a href="{oa["url"]}">merge request !{oa["iid"]}</a> '
        msg += f'at <u><a href="{project["web_url"]}">{project["name"]}</a></u>:'
        msg += "\n"
        msg += f'<pre><code>{oa["title"]}</code></pre>'
    else:
        msg += f'<a href="{oa["url"]}">merge request !{oa["iid"]}</a> '
        if oa[key] == "close" or oa[key] == "update" or oa[key] == "merge":
            msg += f'{oa[key]}d by '
        else:
            msg += f'{oa[key]} by '
        msg += f'<i><b>{user["username"]}</b></i> '
        msg += f'at <u><a href="{project["web_url"]}">{project["name"]}</a></u> '
        if oa[key] == "close" or oa[key] == "closed" :
            msg += "❌"
        if oa[key] == "merge" or oa[key] == "merged":
            msg += "✅"
    return msg