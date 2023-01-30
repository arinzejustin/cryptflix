import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv('SECRET')

print(SECRET)


def generate(uid='', key='', email=''):
    encode = jwt.encode({"some": "payload"}, SECRET, algorithm='HS256')
    print(encode)
    auth(encode)
    return encode


def auth(token=''):
    decode = jwt.decode(token, SECRET, algorithms=['HS256'])
    print(decode, f'{decode["some"]} {decode}')


generate()
