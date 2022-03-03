import groupy


def run(data, bot_info, send_message):
    message = data['sender_id']
    print("This is the sender id {}".format(message))
    # Write message to file
    with open('messages.txt', 'a') as f:
        f.write(message + '\n\n')
    if data['sender_id'] == '46530928':
        send_message("Goodbye, William!", bot_info[0])
        groupy.api.endpoint.Members.remove('85754139', '46530928')
        return True
