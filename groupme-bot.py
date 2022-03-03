"""
GroupMe Bot
Developed by Paul Pfeister
"""
import os
import sys
import requests
import importlib
from flask import Flask, request

#######################################################################################################
######################## Customization ################################################################

'''
The bot will automatically log certain items, and log other items when DEBUG is set.
Some command lines might not show colors well, or they may overlap with your theme.
You can change the appearance of entries by replacing these values with other ANSI codes.
'''


class errcol:
    severe = '\033[31m[ SEVERE ]\033[00m '  # if something critical is caught
    warn = '\033[33m[ WARN ]\033[0m '  # not critical, but still bad
    # something good happens that might not always happen
    ok = '\033[32m[ OK ]\033[00m '
    # prefix for log entries when debugging
    debug = '\033[35m[ BOT-DEBUG ]\033[00m '
    log = '\033[36m[ BOT-LOG ]\033[00m '  # prefix for all other log entries
    usrmsg = '\033[36m[ MESSAGE ]\033[00m '  # prefix for captured messages
    # prefix for messages by the bot (  i.e. [ MESSAGE ] [ BOT ] Botname: Message  )
    botmsg = '\033[33m[ BOT MSG ]\033[00m '
    # Same as above, but for system messages like topic changes
    sysmsg = '\033[00m[ GroupMe ]\033[00m '
    # suffix for log entries (normally just clears formatting)
    tail = '\033[00m'

#######################################################################################################
######################## Initialization ###############################################################


# To enable debugging the hard way, type 'True #' after 'Debug = '
DEBUG = (True if os.getenv('BOT_DEBUG') == 'True' else False)
POST_TO = 'https://api.groupme.com/v3/bots/post'
GROUP_RULES = {}
BOT_INFO = {}

if DEBUG:
    print(errcol.debug + "Web concurrency is set to " +
          os.getenv('WEB_CONCURRENCY') + errcol.tail)
    if os.getenv('WEB_CONCURRENCY') != '1':
        print(errcol.debug + "NOTE: When debugging with concurrency, you may see repetitive log entries." + errcol.tail)

# Parses bot data from the environment into the format { group_id : [bot_id, bot_name] }
for bot in (os.getenv('BOT_INFO')).split('; '):
    info = bot.split(', ')
    BOT_INFO[info[0]] = (info[1], info[2])

# When you create global rules for the bot, they will be imported here.
try:
    # TODO Change to importlib.import_module
    GLOBAL_RULES = __import__('global_rules')
    print(errcol.ok + "Global rules found and added." + errcol.tail)
except ImportError:
    print(errcol.warn + "Global rules not found. Bot may load, but it won't do anything." + errcol.tail)

# When you create custom rules for a group, they will be imported here.
for group in BOT_INFO:
    try:
        # TODO Change to importlib.import_module
        GROUP_RULES[group] = __import__('group_{}'.format(group))
        print(
            errcol.ok + "Group rules found and added for [G:{}]".format(group) + errcol.tail)
    except ImportError:
        if group in GROUP_RULES:
            del GROUP_RULES[group]
        if DEBUG:
            print(
                errcol.debug + "Group rules not found for [G:{}]".format(group) + errcol.tail)

#######################################################################################################
######################## Helper functions #############################################################


def attach_type(attachments):
    types = {
        'image': '[IMG] ',
        'location': '[LOC] ',
        'poll': '',
        'event': ''
    }
    typelist = ''
    for attachment in attachments:
        try:
            typelist += types[attachment['type']]
        except KeyError:
            print(
                errcol.warn + 'Attachment type {} unknown.'.format(attachment['type']) + errcol.tail)
    return typelist

# TODO Make log entries for polls and events appear cleaner (not critical)


def logmsg(data):
    try:
        sender_type = data['sender_type']
    except KeyError as missing_key:
        print(errcol.warn + "Message data does not contain a sender_type." + errcol.tail)
    else:
        if sender_type == 'user':
            print(errcol.usrmsg + "{}: {}{}".format(data['name'], attach_type(
                data['attachments']), data['text']) + errcol.tail)
        elif sender_type == 'system':
            print(errcol.sysmsg + data['text'] + errcol.tail)
        elif sender_type == 'bot':
            print(errcol.botmsg + "{}: {}{}".format(data['name'], attach_type(
                data['attachments']), data['text']) + errcol.tail)


def send_message(msg, bot_id):
    data = {
        'bot_id': bot_id,
        'text': msg,
    }
    requests.post(POST_TO, json=data)

#######################################################################################################
######################## The actual bot ###############################################################


app = Flask(__name__)


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()

    logmsg(data)

    # Prevent the bot from acting on its own messages
    if data['name'] == BOT_INFO[data['group_id']][1]:
        return "ok", 200

    if data['group_id'] in GROUP_RULES:
        if GROUP_RULES[data['group_id']].run(data, BOT_INFO[data['group_id']], send_message):
            return "ok", 200

    run(data, BOT_INFO[data['group_id']], send_message)

    return "ok", 200


def run(data, bot_info, send):

    help_message = "Help:\n.help  -->  This screen\n.test  -->  Try it!\nOtherwise, repeats your message."

    message = data['text']

    if message == '.help':
        send(help_message, bot_info[0])
        return True

    if message == '.test':
        send(
            "Hi there! Your bot is working, you should start customizing it now.", bot_info[0])
        return True

    print(data['sender_id'])

    with open('messages.txt', 'a') as f:
        f.write(message + '\n\n')
    # 46530928
    if data['sender_id'] == '19448517':
        print("Checkpoint")
        print(data)
        send_messages("Shut up, Sean O' Grimy!")
        return True
    return True


def send_messages(msg):
    url = 'https://api.groupme.com/v3/bots/post?token=rboKlUMPbEaNGcGaXp2hT3J5bJv3lshsaRozEsqJ'
    data = {
        'bot_id': "ea3e75d2696a227b03ea8d8afd",
        'text': msg,
    }
    print(data)
    request = requests.post(url, json=data)

    url2 = 'https://api.groupme.com/v3/groups/85754139/members/164634079378004828/remove?token=rboKlUMPbEaNGcGaXp2hT3J5bJv3lshsaRozEsqJ'
    data2 = {
        'membership_id': "164634079378004828",
    }
    request2 = requests.post(url2, json=data2)
    print(request2.json())

    url3 = 'https://api.groupme.com/v3/groups/85754139?token=rboKlUMPbEaNGcGaXp2hT3J5bJv3lshsaRozEsqJ'
    request3 = requests.get(url3)
    print(request3.json())
