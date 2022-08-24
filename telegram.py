import requests


class Telegram:

    def __init__(self):
        self.bot_token = ''
        self.bot_chat_id = ''

    def async_send(self, text):
        send_text = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + self.bot_chat_id + '&parse_mode=Markdown&text=' + text
        requests.get(send_text)

