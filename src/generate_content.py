import logging

from http_util import send_http_request
from response_util import close, elicit_slot, confirm_intent, delegate, initial_message

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# 메시지 내용 생성
def generate_content(intent_request):
    try:
        session_state = intent_request.get('sessionState', {})
        intent = session_state.get('intent', {})
        slots = intent.get('slots', {})

        active_contexts = {}
        confirmation_state = intent.get('confirmationState')
        session_attributes = session_state.get('sessionAttributes', {})

        # 슬롯 값 확인
        message_purpose = try_ex(slots.get('MessagePurpose'))
        message_keyword = try_ex(slots.get('MessageKeyword'))

        if message_purpose and message_keyword:
            active_contexts['MessagePurpose'] = message_purpose
            active_contexts['MessageKeyword'] = message_keyword

            if confirmation_state == 'None':
                return delegate(
                    session_attributes,
                    active_contexts,
                    intent,
                    '메시지 내용을 생성하시겠습니까?'
                )

            elif confirmation_state == 'Confirmed':
                intent['confirmationState'] = 'Confirmed'
                intent['state'] = 'Fulfilled'

                message = http_request(session_attributes, slots)
                return close(
                    session_attributes,
                    active_contexts,
                    'Fulfilled',
                    intent,
                    message
                )
    except Exception as e:
        logger.error(f"메시지 내용 생성 중 오류 발생: {str(e)}")
        return close(
            {},
            {},
            'Failed',
            {},
            '메시지 내용 생성 중 오류가 발생했습니다.'
        )


def http_request(session_attributes, slots):
    # HTTP 요청
    url = 'https://dev.enble.site/api/ai_messages'

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

    return message


def try_ex(value):
    if isinstance(value, dict):
        return value.get('value', {}).get('interpretedValue')
    return None
