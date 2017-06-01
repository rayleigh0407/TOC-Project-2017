import sys
from io import BytesIO

import urllib.request
import re

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine
from fsm import data_build

text = urllib.request.urlopen("http://127.0.0.1:4040").read()
url = re.search(b"https://([A-Za-z0-9]+)\.ngrok\.io", text)

API_TOKEN = '332972762:AAFdcV3Wiq_dQWtbLT7y_9hhUujxtkSDCgA'
WEBHOOK_URL = url.group(0).decode('utf-8') + '/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'start',
        'user',
        'search',
        'search_mid',
        'search_end',
        'calendar',
        'calendar_end',
        'black',
        'black_end'
    ],
    transitions=[
        # start action
        {
            'trigger': 'advance',
            'source': 'start',
            'dest': 'user',
            'conditions': 'bot_init'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'search',
            'conditions': 'is_going_to_search'
        },
        {
            'trigger': 'advance',
            'source': 'search',
            'dest': 'search_mid',
            'conditions': 'is_going_to_search_mid'
        },
        {
            'trigger': 'advance',
            'source': 'search_mid',
            'dest': 'search_end',
            'conditions': 'is_going_to_search_end'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'calendar',
            'conditions': 'is_going_to_calendar'
        },
        {
            'trigger': 'advance',
            'source': 'calendar',
            'dest': 'calendar_end',
            'conditions': 'is_going_to_calendar_end'
        },
        {
            'trigger': 'advance',
            'source': 'user',
            'dest': 'black',
            'conditions': 'is_going_to_black'
        },
        {
            'trigger': 'advance',
            'source': 'black',
            'dest': 'black_end',
            'conditions': 'is_going_to_black_end'
        },
        {
            'trigger': 'go_back',
            'source': [
                'search_end',
                'calendar_end',
                'black_end'
            ],
            'dest': 'user'
        }
    ],
    initial='start',
    auto_transitions=False,
    show_conditions=True,
)



def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    data_build()
    app.run()