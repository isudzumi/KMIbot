import os
import logging
from linebot import (
    LineBotApi,  WebhookHandler
)
from linebot.models import (
    TextSendMessage, MessageEvent, TextMessage
)
from linebot.exceptions import (
    InvalidSignatureError,
    LineBotApiError
)
import transform

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

LINE_ACCESS_TOKEN=os.environ['LINE_ACCESS_TOKEN']
LINE_CHANNEL_SECRET=os.environ['LINE_CHANNEL_SECRET']
MAGIC_KEYWORD=os.environ['MAGIC_KEYWORD']

line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


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


@handler.add(MessageEvent, message=TextMessage)
def reply_message(line_event):
    text = line_event.message.text
    if (not text.startswith(MAGIC_KEYWORD)):
        return
    input_text = text.removeprefix(MAGIC_KEYWORD)
    if (not input_text):
        return
    logger.info(input_text)
    generated_text = transform.generate(input_text)
    logger.info(generated_text)
    line_bot_api.reply_message(
        line_event.reply_token,
        TextSendMessage(text=generated_text)
    )


def lambda_handler(event, _):
    try:
        signature = event['headers'].get('x-line-signature')
        logger.info(signature)
        if (not signature):
            return create_lambda_response(403)
        body = event['body']
        logger.debug(f'Event body type: {type(body)}')

        handler.handle(body, signature)

        return create_lambda_response(200)
    except InvalidSignatureError:
        logger.error('Invalid Signature Error')
        return create_lambda_response(400)
    except LineBotApiError as e:
        for m in e.error.details:
            logger.error(f'LINE Bot API Error: {m.property} {m.message}')
        return create_lambda_response(500)


if __name__ == '__main__':
    pass
