import groupy


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

    if data['sender_id'] == '46530928':
        send("Goodbye, William!", bot_info[0])
        groupy.api.endpoint.Members.remove('85754139', '46530928')
        return True
    return True
