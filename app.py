import os
import base64
import hashlib
import hmac
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.models import TextSendMessage
from linebot.exceptions import (
    InvalidSignatureError
)
import transform

ACCESS_TOKEN=os.environ['ACCESS_TOKEN']
CHANNEL_SECRET=os.environ['CHANNEL_SECRET']
KEYWORD='亀井！'

line_bot_api = LineBotApi(ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

def validate_signature(event):
    hash = hmac.new(CHANNEL_SECRET.encode('utf-8'),
            event.body.encode('utf-8'),hashlib.sha256).digest()
    signature = base64.b64encode(hash)
    if (event.headers['X-Line-Signature'] != signature):
        raise InvalidSignatureError

def handle(event):
    try:
        validate_signature(event)
        message = event.message.text
        if (not message.startswith(KEYWORD)):
            return {}
        text = transform.generate(message.removeprefix(KEYWORD))
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=text)
        )
    except InvalidSignatureError:
        return {
            'statusCode': 400
        }

if __name__ == '__main__':
    pass
