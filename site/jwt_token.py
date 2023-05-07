import json
import jwt, os, random, time
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

SECRET = os.getenv('SECRET')


def generate(uuid: str, key: str, email: str, name: str, ssid: str):
    """
    The function generates a JWT token with given parameters and returns it.
    
    :param uuid: A string representing a unique identifier for a user
    :type uuid: str
    :param key: The key parameter is a string that is used as a secret key to encode the JWT token. It
    should be kept secret and not shared with anyone
    :type key: str
    :param email: The email parameter is a string that represents the email address of the user
    :type email: str
    :param name: The name of the user for whom the JWT token is being generated
    :type name: str
    :param ssid: The parameter "ssid" is a string that represents the session ID of the user. It is used
    to identify and track the user's session on the website or application
    :type ssid: str
    :return: a JWT token encoded with the provided parameters (uuid, key, email, name, ssid) and a set
    of additional claims (exp, iat, sub, iss) using the HS256 algorithm and a secret key. If any of the
    required parameters are missing, the function returns None.
    """
    if not uuid or not key or not email or not name or not ssid:
        return None
    encode = jwt.encode({"uuid": str(uuid), 'ssid': str(ssid), "key": str(key), "name": str(name), "email": str(email), 'exp': datetime.utcnow() + timedelta(hours=1), 'iat': datetime.utcnow(), 'sub': f'{email} token', 'iss': 'cryptflixinvest.com'}, SECRET, algorithm='HS256')
    return encode


def authenticate(token: str):
    """
    The function takes a token string, decodes it using a secret key, and returns the decoded
    information or None if there is an exception.
    
    :param token: The token parameter is a string that represents a JSON Web Token (JWT) that is used
    for authentication purposes. The function attempts to decode the token using a secret key and the
    HS256 algorithm. If the decoding is successful, the function returns the decoded token, which
    contains information about the user. If
    :type token: str
    :return: either the decoded token (if it is valid and can be decoded using the provided secret key)
    or None (if the token is invalid or cannot be decoded).
    """
    try:
       decode = jwt.decode(token, SECRET, algorithms=['HS256'])
       return decode
    except Exception as e:
        print(str(e))
        return None


def authorize(cookie: dict, token: str):
    """
    The function checks if the provided cookie and token are authorized based on their UUID, SSID, and
    issuer.
    
    :param cookie: The "cookie" parameter is likely an object that contains information about the user's
    session, such as a unique identifier (UUID) and a session ID (SSID). This information is typically
    stored in a cookie on the user's browser and is used to authenticate the user's requests to the
    server
    :param token: The `token` parameter is a string representing a JSON Web Token (JWT) that is used for
    authentication. It contains information about the user and their session, such as the user ID,
    session ID, and expiration time
    :type token: str
    :return: a boolean value (True or False) depending on whether the conditions in the if statements
    are met or not.
    """
    jwt = authenticate(token=token)
    if jwt is None:
        return False
    if cookie['uuid'] != jwt['uuid'] or cookie['ssid'] != jwt['ssid'] or jwt['iss'] != 'cryptflixinvest.com':
        return False
    return True


def acct_token():
    """
    It generates a random number between 100000 and 999999 and returns it
    :return: A random number between 100000 and 999999
    """
    token = random.randrange(100000, 999999)
    expires = int(time.time() * 1000 + 3000000)
    return dict(token=token, expires=expires)
