import logging
from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import requests
import os

app = Flask(__name__)

ask = Ask(app, "/")

logger = logging.getLogger()


@ask.launch
def launch():
    return ark_price()


@ask.intent("ArkPriceIntent")
def ark_price():
    r = requests.get("https://api.coinmarketcap.com/v1/ticker/ark/")
    if r.status_code == 200:
        price = r.json()[0]["price_usd"]
        speech = "The price of Ark is {0} $".format(price)
    logger.info('speech = {}'.format(speech))
    return statement(speech)


@ask.intent('AMAZON.HelpIntent')
def help():
    speech_text = 'You can say hello to me!'
    return question(speech_text).reprompt(speech_text).simple_card('ArkPrice', speech_text)


@ask.session_ended
def session_ended():
    return "{}", 200

if __name__ == '__main__':
    if 'ASK_VERIFY_REQUESTS' in os.environ:
        verify = str(os.environ.get('ASK_VERIFY_REQUESTS', '')).lower()
        if verify == 'false':
            app.config['ASK_VERIFY_REQUESTS'] = False
    app.run(debug=True)