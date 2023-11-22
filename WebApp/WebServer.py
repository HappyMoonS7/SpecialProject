
from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import (MessageEvent, TextMessage, TextSendMessage,BeaconEvent)

app = Flask(__name__)

line_bot_api = LineBotApi('KwOqh2ygwm/ZEELgTi8wcHx1ZTOnjkddJA1rzjBKRan7OezkRaJtstVGsgTYgtjD2KijQCS6aGsea7ivdDyQ+GX2uvE+pjqubAyokDi3VtPyN3KgFTmIFySsPMDiiKOmshW43V8evvJHx/ZWAw/j2wdB04t89/1O/w1cDnyilFU=')#YOUR_CHANNEL_ACCESS_TOKEN
handler = WebhookHandler('60b52a19ff41f94dde3df82e39789686')#YOUR_CHANNEL_SECRET

@app.route("/")
def hello():
    return "hi"

@app.route("/webhook",methods=['GET','POST'])
def webhook():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'
    

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="Chatนี้สำหรับการแจ้งเตือนเหตุเท่านั้น"))




@handler.add(BeaconEvent)
def handle_beacon(event):
    line_bot_api.broadcast(TextSendMessage(text='found at office room 2nd floor'))
    
    # line_bot_api.reply_message(
    #     event.reply_token,
    #     TextSendMessage(
    #         text='Got beacon event. hwid={}, device_message(hex string)={}'.format(
    #             event.beacon.hwid, event.beacon.dm)))

if __name__ == "__main__":
    app.run()