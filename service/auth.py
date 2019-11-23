import jwt
import datetime as dt

from service import app

PASS_KEY = 'JWT-SECRET-PASS'

def decode_auth_token(auth_token):
    """
    Validates the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, PASS_KEY)
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise
    except jwt.InvalidTokenError:
        raise


def encode_auth_token(user_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': dt.datetime.utcnow() + dt.timedelta(hours=1),
            'iat': dt.datetime.utcnow(),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            PASS_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        return e