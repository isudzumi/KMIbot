import os
import json
import logging
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

LINE_ACCESS_TOKEN=os.environ['LINE_ACCESS_TOKEN']
LINE_CHANNEL_SECRET=os.environ['LINE_CHANNEL_SECRET']
MAGIC_KEYWORD=os.environ['MAGIC_KEYWORD']

line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
parser = WebhookParser(LINE_CHANNEL_SECRET)

def create_lambda_response(statusCode: int):
    """ Create output for Lambda Proxy Integration
    Generate the output format for Lambda Proxy Integration
    ref. https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html

    :param int statusCode: http status code
    """
    return {
        'isBase64Encoded': False,
        'statusCode': statusCode,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': '{}'
    }

def handler(event, context):
    try:
        signature = event['headers'].get('x-line-signature')
        logging.info(signature)
        if (not signature):
            return create_lambda_response(403)
        events = parser.parse(json.dumps(event['body']), signature)
        
        for event in events:
            if not isinstance(event, MessageEvent):
                continue
            if not isinstance(event.message, TextMessage):
                continue
            message = event.message.text
            if (not message.startswith(MAGIC_KEYWORD)):
                continue
            input_text = message.removeprefix(MAGIC_KEYWORD)
            if (not input_text):
                continue
            logging.info(input_text)
            text = transform.generate(input_text)
            logging.info(text)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=text)
            )

        return create_lambda_response(200)
    except InvalidSignatureError:
        logging.error('Invalid Signature Error')
        return create_lambda_response(400)

if __name__ == '__main__':
    pass
