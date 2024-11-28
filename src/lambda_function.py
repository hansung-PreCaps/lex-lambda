import logging

from jwt_util import verify_jwt
from response_util import close, elicit_slot, confirm_intent, delegate, initial_message
from generate_content import generate_content
from generate_image import generate_image

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# Main Handler
def lambda_handler(event, context):
    return dispatch(event)


def dispatch(intent_request):
    logger.debug(intent_request)

    intent_name = intent_request['sessionState']['intent']['name']
    intent = intent_request['sessionState']['intent']
    slots = intent['slots']

    message_purpose = slots['MessagePurpose'] if 'MessagePurpose' in slots else None
    message_keyword = slots['MessageKeyword'] if 'MessageKeyword' in slots else None


    # JWT 토큰 검증
    if not verify_jwt(intent_request):
        return close({}, {}, 'Failed', intent, '먼저 로그인 해주세요. (JWT 토큰 없음)')

    if not isinstance(message_keyword, type(None)) or not isinstance(message_purpose, type(None)):
        # Dispatch to bot's intent handlers
        if intent_name == 'GenerateMessageContent':
            return generate_content(intent_request)
        if intent_name == 'GenerateImage':
            return generate_image(intent_request)

        raise Exception('Intent name : ' + intent_name + 'is not supported')
