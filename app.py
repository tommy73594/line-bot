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

app = Flask(__name__)

line_bot_api = LineBotApi('MDXe+wZjmWuB0KRa89WPYAPvzCmC7/CwxJl43i8x/qrsAnfs+28B1KbvaPLc42wtia2sWVODQZx/eFky3KmM09IPu5NVI+8nx97gx8pqYtrA5b9e7lwKE/qkwE2Z6gj9NE0Dh8RLL0HTafjMFV2aXwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('84588ee3fb4ab427534fd2ad33dcb1d3')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()