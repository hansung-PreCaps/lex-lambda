import os
import jwt
import logging
import base64

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

JWT_SECRET_KEY = base64.b64decode(os.getenv("JWT_SECRET_KEY"))


def verify_jwt(event):
    try:
        session_attributes = event['sessionState'].get('sessionAttributes', {})
        access_token = session_attributes.get('Authorization')

        if not access_token:
            return False

        if access_token.startswith('Bearer '):
            token = access_token.split(' ')[1]
        else:
            token = access_token

        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=["HS256"],
            options={"verify_sub": True}
        )

        # email claim이 없으면 에러
        if 'email' not in payload:
            logger.error("Missing email claim")
            return False

        # test
        logger.debug(payload)

        return True

    except jwt.ExpiredSignatureError:
        logger.error("JWT token has expired")
    except jwt.InvalidTokenError:
        logger.error("Invalid JWT token")
    except Exception as e:
        logger.error(f"JWT verification error: {str(e)}")

    return False