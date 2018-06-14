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
import socket
import binascii
import json

app = Flask(__name__)
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

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

@app.route("/iwana")
def iwana():
    x = {}
    x["iwana_now"] = iwana_now()
    return json.dumps(x)

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))

def iwana_now():
    data = "1900d402123138377365727665722e78797a00464d4c0063dd01010009010000000006452306"
    data = binascii.unhexlify(data)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("187server.xyz" ,25565))
    client.send(data)
    response = client.recv(1024)
    ans = binascii.hexlify(response)[10:]
    ans = binascii.unhexlify(ans).decode('utf-8', 'replace') + '"}'
    ans = json.loads(ans)["players"]["online"]
    client.close()
    return ans
    
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
