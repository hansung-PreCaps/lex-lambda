import logging

from http_util import send_http_request
from response_util import close, elicit_slot, confirm_intent, delegate, initial_message

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# 메시지 내용 생성
def generate_content(intent_request):
    session_state = intent_request.get('sessionState', {})
    intent = session_state.get('intent', {})
    slots = intent.get('slots', {})

    active_contexts = {}
    confirmation_state = intent.get('confirmationState')

    url = 'https://dev.enble.site/api/ai_messages'

    session_attributes = session_state.get('sessionAttributes', {})
    access_token = session_attributes.get('Authorization')

    # Bearer 토큰 형식 확인 및 수정
    if access_token and not access_token.startswith('Bearer '):
        access_token = f'Bearer {access_token}'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': access_token
    }

    body = {
        'situation': slots.get('MessagePurpose', {}).get('value', {}).get('interpretedValue', ''),
        'keyword': [slots.get('MessageKeyword', {}).get('value', {}).get('interpretedValue', '')]
    }

    logger.debug(f"API 요청: {body}")

    message = send_http_request('POST', url, body, headers)

    return close(
        session_attributes,
        active_contexts,
        'Fulfilled',
        intent,
        message
    )


def try_ex(value):
    if value is not None:
        return value['value']['interpretedValue']
    else:
        return None
