import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv('SECRET')


def generate(uuid: str = '', key: str = '', email: str = ''):
    if not uuid or not key or not email:
        return
    encode = jwt.encode({"some": "payload"}, SECRET, algorithm='HS256')
    return encode


def authenticate(token: str = ''):
    decode = jwt.decode(token, SECRET, algorithms=['HS256'])
    print(decode, f'{decode["some"]} {decode}')


def authorize(cookie, token):
    return
