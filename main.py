from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

import os

# my module
from iwana.iwana import iwana

app = Flask(__name__)
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

# twitter
twCONSUMER_KEY = os.environ['twCONSUMER_KEY']
twCONSUMER_SECRET = os.environ['twCONSUMER_SECRET']
CALLBACK_URL = 'https://nazotest001.herokuapp.com/'
app.config['twSECRET_KEY'] = os.urandom(24)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

app.register_module(iwana, url_prefix='/iwana')


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    x = event.message.text
    if x == 'iwana' or x == 'いわな':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=iwana.iwana.iwana()))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))


    
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
