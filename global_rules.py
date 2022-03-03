import os

from urllib.parse import urlencode
from urllib.request import Request, urlopen

POST_TO = 'https://api.groupme.com/v3/bots/post?token=rboKlUMPbEaNGcGaXp2hT3J5bJv3lshsaRozEsqJ'


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
    if data['sender_id'] == '19448517':
        print("Checkpoint")
        send_message("Goodbye, Bill!", bot_info[0])
        return True

    send("Hi {}! You said: {}".format(data['name'], data['text']), bot_info[0])
    return True


def send_message(msg, bot_info):
    url = 'https://api.groupme.com/v3/bots/post'

    data = {
        'bot_id': bot_info[0],
        'text': msg,
    }
    request = Request(url, urlencode(data).encode())
    json = urlopen(request).read().decode()
