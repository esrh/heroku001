from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os, json

# my module
from iwana import iwana
from tw import tw, tw_auth

app = Flask(__name__)

app.register_blueprint(iwana.app)
app.register_blueprint(tw.app)

app.config['SECRET_KEY'] = "wiufgb8h23487nyv785ty238c7t74ngry7c3ngr67ygn437nfr6yghy8f43g"

try:
    line_bot_api = LineBotApi(os.environ["YOUR_CHANNEL_ACCESS_TOKEN"])
    handler = WebhookHandler(os.environ["YOUR_CHANNEL_SECRET"])
except:
    with open(os.path.expanduser('~/pass/token.json'), 'r') as f:
        hoge = json.load(f)["line"]
        line_bot_api, handler = LineBotApi(hoge["token"]), WebhookHandler(hoge["secret"])


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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    x = event.message.text
    if x == 'iwana' or x == 'いわな':
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=iwana.iwanafunc()))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))


    
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, threaded=True)
