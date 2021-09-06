import os
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.models import (
    TextSendMessage, MessageEvent, TextMessage
)
from linebot.exceptions import (
    InvalidSignatureError
)
import transform

ACCESS_TOKEN=os.environ['ACCESS_TOKEN']
CHANNEL_SECRET=os.environ['CHANNEL_SECRET']
KEYWORD=os.environ['KEYWORD']

line_bot_api = LineBotApi(ACCESS_TOKEN)
parser = WebhookParser(CHANNEL_SECRET)

def create_lambda_response(statusCode: int):
    """ Create output for Lambda Proxy Integration
    Generate the output format for Lambda Proxy Integration
    ref. https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-output-format

    :param int statusCode: http status code
    """
    return {
        'isBase64Encoded': False,
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': {}
    }

def handler(event, context):
    try:
        signature = event['headers'].get('x-line-signature')
        if (not signature):
            return create_lambda_response(403)
        events = parser.parse(event.body, signature)
        
        for event in events:
            if not isinstance(event, MessageEvent):
                continue
            if not isinstance(event.message, TextMessage):
                continue
            message = event.message.text
            if (not message.startswith(KEYWORD)):
                continue
            text = transform.generate(message.removeprefix(KEYWORD))
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=text)
            )

        return create_lambda_response(200)
    except InvalidSignatureError:
        return create_lambda_response(400)

if __name__ == '__main__':
    pass
