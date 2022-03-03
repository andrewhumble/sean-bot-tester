import groupy


def run(data, bot_info, send_message):
    print(data)
    message = data
    # Write message to file
    with open('messages.txt', 'a') as f:
        f.write(message + '\n\n')
    if data['sender_id'] == '644916880':
        send_message("Goodbye, Sean!")
        groupy.api.endpoint.Members.remove('85754139', '644916880')
        return True
