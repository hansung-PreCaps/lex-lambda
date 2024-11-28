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
            response_body = json.loads(response.data.decode('utf-8'))
            message = response_body.get('result').get('message')
        else:
            message = f'API 요청 실패: HTTP {response.status}'
    except Exception as e:
        logger.error(f"API 요청 중 오류 발생: {str(e)}")
        message = '서버 연결 중 오류가 발생했습니다.'

    return message