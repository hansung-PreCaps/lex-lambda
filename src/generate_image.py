import logging

from http_util import send_http_request
from response_util import close, elicit_slot, confirm_intent, delegate, initial_message

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# 이미지 생성
def generate_image(intent_request):
    try:
        session_state = intent_request.get('sessionState', {})
        intent = session_state.get('intent', {})
        slots = intent.get('slots', {})

        active_contexts = {}
        session_attributes = session_state.get('sessionAttributes', {})

        # 슬롯 값 확인
        situation = try_ex(slots.get('Situation'))
        atmosphere = try_ex(slots.get('Atmosphere'))

        # 슬롯 값이 없는 경우 요청
        if situation is None:
            return elicit_slot(
                session_attributes,
                active_contexts,
                intent,
                'situation',
                '이미지를 생성할 목적을 알려주세요.'
            )

        if atmosphere is None:
            return elicit_slot(
                session_attributes,
                active_contexts,
                intent,
                'atmosphere',
                '이미지를 생성할 분위기를 알려주세요.'
            )

        # 슬롯 값이 있는 경우 이미지 생성
        if situation and atmosphere:
            active_contexts['Situation'] = situation
            active_contexts['Atmosphere'] = atmosphere

            intent['confirmationState'] = 'Confirmed'
            intent['state'] = 'Fulfilled'

            message = http_request(session_attributes, slots)

            # test
            logger.debug(f"Generated message: {message}")

            return close(
                session_attributes,
                active_contexts,
                'Fulfilled',
                intent,
                {
                    message,
                    {
                        'contentType': 'PlainText',
                        'content': '생성된 이미지가 마음에 들지 않으시다면, 언제든 다시 대화를 시작해주세요.'
                    }
                }
            )
    except Exception as e:
        logger.error(f"Intent 처리 중 오류 발생: {str(e)}")


def http_request(session_attributes, slots):
    # HTTP 요청
    url = 'https://dev.enble.site/api/images'

    access_token = session_attributes.get('Authorization')

    # Bearer 토큰 형식 확인 및 수정
    if access_token and not access_token.startswith('Bearer '):
        access_token = f'Bearer {access_token}'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': access_token
    }

    body = {
        'situation': slots.get('Situation', {}).get('value', {}).get('interpretedValue', ''),
        'atmosphere': slots.get('Atmosphere', {}).get('value', {}).get('interpretedValue', '')
    }

    logger.debug(f"API 요청: {body}")

    message = send_http_request('POST', url, body, headers)
    image_url = message.get('result').get('url')

    return image_url


def try_ex(value):
    if isinstance(value, dict):
        return value.get('value', {}).get('interpretedValue')
    return None
