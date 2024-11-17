import logging
import urllib3
import json

from response_util import close, elicit_slot, confirm_intent, delegate, initial_message

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


# 메시지 내용 생성
def generate_content(intent_request):
    http = urllib3.PoolManager()
    url = 'https://dev.enble.site/api/ai_messages'

    intent = intent_request['sessionState']['intent']

    session_attributes = intent_request['sessionState'].get('sessionAttributes', {})
    access_token = session_attributes.get('Authorization', '')

    # Bearer 토큰 형식 확인 및 수정
    if access_token and not access_token.startswith('Bearer '):
        access_token = f'Bearer {access_token}'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': access_token
    }

    body = {
        'situation': intent['slots'].get('MessagePurpose', {}).get('value', '').get('interpretedValue', ''),
        'keyword': [intent['slots'].get('MessageKeyword', {}).get('value', '').get('interpretedValue', '')]
    }

    logger.debug(f"API 요청: {body}")

    try:
        response = http.request(
            'POST',
            url,
            body=json.dumps(body),
            headers=headers
        )

        if response.status == 200:
            result = json.loads(response.data.decode('utf-8'))
            message = result.get('message', 'API 요청 성공')

            logger.debug(f"API 응답: {result}")
        else:
            message = f'API 요청 실패: HTTP {response.status}'

    except Exception as e:
        logger.error(f"API 요청 중 오류 발생: {str(e)}")
        message = '서버 연결 중 오류가 발생했습니다.'

    active_contexts = {}
    # confirmation_status = intent_request['sessionState']['intent']['confirmationState']

    return close(
        session_attributes,
        active_contexts,
        'Fulfilled',
        intent,
        message
    )
