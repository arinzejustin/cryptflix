import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET = os.getenv('SECRET')


def generate(uuid: str, key: str, email: str, name: str):
    """
    It takes in a uuid, key, email, and name, and returns a JWT token
    
    :param uuid: The user's unique ID
    :type uuid: str
    :param key: The key that the user will use to access the API
    :type key: str
    :param email: the email of the user
    :type email: str
    :param name: The name of the user
    :type name: str
    :return: A string
    """
    if not uuid or not key or not email or not name:
        return
    encode = jwt.encode({"some": "payload"}, SECRET, algorithm='HS256')
    return encode


def authenticate(token: str):
    decode = jwt.decode(token, SECRET, algorithms=['HS256'])
    print(decode, f'{decode["some"]} {decode}')


def authorize(cookie, token):
    return
