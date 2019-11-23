import jwt
import datetime as dt

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


def validate_token(auth_header, user_id):
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except IndexError:
            raise MalformedBearerTokenError('Bearer token malformed!')
    else:
        auth_token = ''

    if auth_token:
        try:
            res = int(user_id) == int(decode_auth_token(auth_token))
            if not res:
                raise NotValidTokenError('Provide a valid auth token!')
        except (jwt.InvalidTokenError, jwt.ExpiredSignatureError):
            raise NotValidTokenError('Provide a valid auth token!')
    else:
        raise NotValidTokenError('Provide a valid auth token!')


class MalformedBearerTokenError(Exception):
    def __init__(self, value):
        self.value = value


class NotValidTokenError(Exception):
    def __init__(self, value):
        self.value = value
