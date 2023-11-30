import jwt

from main_info import settings


def get_domain():
    return 'http://127.0.0.1:8000'


def generate_token(**kwargs):
    token = jwt.encode(
        kwargs,
        settings.SECRET_KEY,
        algorithm="HS256"
    )

    return token


def decode_token(token):
    data = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=["HS256"]
    )

    return data
