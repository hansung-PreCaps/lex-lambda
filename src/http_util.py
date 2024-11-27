import logging
import urllib3
import json

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def send_http_request(method, url, body, headers):
    http = urllib3.PoolManager()
    try:
        response = http.request(
            method,
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

    return message