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
    modified_files = 0
    added_files = 0
    removed_files = 0
    if len(data["commits"]):
        for commit in data["commits"]:
            modified_files += len(commit["added"])
            added_files += len(commit["modified"])
            removed_files += len(commit["removed"])
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
    if modified_files:
        msg += f'{modified_files} '
        if not info_added:
            if modified_files > 1:
                msg += "files "
            else:
                msg += "file "
        msg += "modified "
        info_added = True
    if added_files:
        msg += f'{added_files} '
        if not info_added:
            if added_files > 1:
                msg += "files "
            else:
                msg += "file "
        msg += "added "
        info_added = True
    if removed_files:
        msg += f'{removed_files} '
        if not info_added:
            if removed_files > 1:
                msg += "files "
            else:
                msg += "file "
        msg += "removed"
    return msg


def generateIssueMsg(data):
    action = data['object_attributes']['action']
    if action == 'open':
        assignees = ''
        for assignee in data.get('assignees', []):
            assignees += assignee['name'] + ' '
        msg = '*{0}* new issue for *{1}*:\n'\
            .format(data['project']['name'], assignees)
    elif action == 'reopen':
        assignees = ''
        for assignee in data.get('assignees', []):
            assignees += assignee['name'] + ' '
        msg = '*{0}* issue re-opened for *{1}*:\n'\
            .format(data['project']['name'], assignees)
    elif action == 'close':
        msg = '*{0}* issue closed by *{1}*:\n'\
            .format(data['project']['name'], data['user']['name'])
    elif action == 'update':
        assignees = ''
        for assignee in data.get('assignees', []):
            assignees += assignee['name'] + ' '
        msg = '*{0}* issue assigned to *{1}*:\n'\
            .format(data['project']['name'], assignees)

    msg = msg + '[{0}]({1})'\
        .format(data['object_attributes']['title'], data['object_attributes']['url'])
    return msg


def generateCommentMsg(data):
    ntype = data['object_attributes']['noteable_type']
    if ntype == 'Commit':
        msg = 'note to commit'
    elif ntype == 'MergeRequest':
        msg = 'note to MergeRequest'
    elif ntype == 'Issue':
        msg = 'note to Issue'
    elif ntype == 'Snippet':
        msg = 'note on code snippet'
    return msg


def generateMergeRequestMsg(data):
    user = data["user"]
    project = data["project"]
    msg = ""

    oa = data["object_attributes"]
    if oa["action"] == "open" or oa["action"] == "reopen":
        msg += f'<i><b>{user["username"]}</b></i> '
        msg += f'{oa["action"]}ed '
        msg += f'<a href="{oa["url"]}">merge request !{oa["iid"]}</a> '
        msg += f'at <u><a href="{project["web_url"]}">{project["name"]}</a></u>:'
        msg += "\n"
        msg += f'<pre><code>{oa["title"]}</code><pre>'
    else:
        msg += f'<a href="{oa["url"]}">merge request !{oa["iid"]}</a> '
        if oa["action"] == "approved" or oa["action"] == "unapproved":
            msg += f'{oa["action"]} by '
        else:
            msg += f'{oa["action"]}d by '
        msg += f'<i><b>{user["username"]}</b></i> '
        msg += f'at <u><a href="{project["web_url"]}">{project["name"]}</a></u> '
        if oa["action"] == "close":
            msg += "❌"
        if oa["action"] == "merge":
            msg += "✅"
    return msg


def generateWikiMsg(data):
    return 'new wiki stuff'


def generatePipelineMsg(data):
    return 'new pipeline stuff'


def generateBuildMsg(data):
    return 'new build stuff'