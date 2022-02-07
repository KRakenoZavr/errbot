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
        if kind == 'push':
            msg = generatePushMsg(data)
        elif kind == 'tag_push':
            msg = generatePushMsg(data)  # TODO:Make own function for this
        elif kind == 'issue':
            msg = generateIssueMsg(data)
        elif kind == 'note':
            msg = generateCommentMsg(data)
        elif kind == 'merge_request':
            msg = generateMergeRequestMsg(data)
        elif kind == 'wiki_page':
            msg = generateWikiMsg(data)
        elif kind == 'pipeline':
            msg = generatePipelineMsg(data)
        elif kind == 'build':
            msg = generateBuildMsg(data)
        self.send_to_chats(msg)
        return jsonify({'status': 'ok'})

    def send_to_chats(self, msg):
        self.send(
            self.build_identifier("-732525540"),
            msg
        )


def generatePushMsg(data):
    msg = '*{0} ({1}) - {2} new commits*\n'\
        .format(data['project']['name'], data['project']['default_branch'], data['total_commits_count'])
    for commit in data['commits']:
        msg = msg + '----------------------------------------------------------------\n'
        msg = msg + commit['message'].rstrip()
        msg = msg + '\n' + commit['url'].replace("_", "\_") + '\n'
    msg = msg + '----------------------------------------------------------------\n'
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
    return 'new MergeRequest'


def generateWikiMsg(data):
    return 'new wiki stuff'


def generatePipelineMsg(data):
    return 'new pipeline stuff'


def generateBuildMsg(data):
    return 'new build stuff'