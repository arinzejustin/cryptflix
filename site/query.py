import mysql.connector as mc
import os
import uuid
import time
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash

from jwt_token import generate, acct_token
from netrequest import post, get

load_dotenv()

HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')
PORT = os.getenv('PORT')
SALT = os.getenv('SALT')
EMAIL_URL = os.getenv('EMAIL_URL')
SERVER_KEY = os.getenv('SERVER_KEY')

mydb = mc.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    port=PORT,
    database=DB_NAME
)

cursor = mydb.cursor()


def db_login(email: str, password: str):
    """
    It takes in an email and password, checks if the email exists in the database, if it does, it checks
    if the password matches the hashed password in the database, if it does, it generates a token and
    returns a dictionary with the token and other details.

    :param email: str, password: str
    :type email: str
    :param password: the password entered by the user
    :type password: str
    :return: A dictionary
    """
    try:
        query = "SELECT * FROM users WHERE email = %s"
        value = (email,)
        cursor.execute(query, value)
        user = cursor.fetchone()
        if user:
            verify = check_password_hash(user[4], password)
            if verify:
                token = generate(
                    uuid=user[1], email=email, key=user[0], name=user[2])
                result = dict(message='Login successful', status=True, uuid=user[1], account=user[7], name=user[2], email=email,
                              bearer=token)
                return result
            else:
                result = dict(message='Invalid credentials',
                              status=False, link=2)
                return result
        else:
            result = dict(message='User not found', status=False)
            return result
    except:
        return except_func('Login')


def db_onboard(email: str, name: str, tel: str):
    """
    It inserts a new user into the database

    :param email: str, name: str, tel: str
    :type email: str
    :param name: str, email: str, tel: str, insert: bool
    :type name: str
    :param tel: str
    :type tel: str
    :return: A dictionary with the keys 'message' and 'status'
    """
    try:
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            if account[4] is None:
                return dict(message='Set your passcode', status=True, double=True, uuid=account[1])
            return dict(message='Account already exists!', status=False)
        query = 'INSERT INTO users (uuid, name, email, tel) VALUES (%s, %s, %s, %s)'
        uid = uuid.uuid4().hex
        values = (uid, name, email, tel)
        cursor.execute(query, values)
        mydb.commit()
        onboard = db_verify(email=email, insert=True)
        if onboard['status']:
            try:
                cursor.execute(
                    f'CREATE TABLE user_{uid} (ID INT AUTO_INCREMENT PRIMARY KEY, ADDRESS VARCHAR(255), TRANSACTION VARCHAR(100), STATUS VARCHAR(100), TIME VARCHAR(100), TYPE VARCHAR(100), THEME VARCHAR(10), TRANS_PASS VARCHAR(100))')
                cursor.execute('UPDATE user_' + uid +
                               ' SET TYPE = %s', ('Plan 1',))
                mydb.commit()
                onboard.update({'uuid': uid})
            except:
                query = "DELETE FROM users WHERE uuid = %s"
                value = (uid, )
                cursor.execute(query, value)
                mydb.commit()
                return except_func('Accounts')
        else:
            query = "DELETE FROM users WHERE uuid = %s"
            value = (uid, )
            cursor.execute(query, value)
            mydb.commit()
        return onboard
    except:
        query = "DELETE FROM users WHERE email = %s"
        value = (email, )
        cursor.execute(query, value)
        mydb.commit()
        return except_func('Sign up')


def db_verify(email: str, insert: bool, code: str = ''):
    """
    It takes an email, a boolean, and a code. If the boolean is true, it inserts a token into the
    database. If the boolean is false, it checks if the code is valid.

    :param email: str = The email of the user
    :type email: str
    :param insert: bool
    :type insert: bool
    :param code: str = ''
    :type code: str
    :return: A dictionary with the keys 'message' and 'status'
    """
    if insert:
        try:
            query = "UPDATE users SET code = %s WHERE email = %s"
            token = acct_token()
            values = (f"{token['token']}:{token['expires']}", email)
            cursor.execute(query, values)
            mydb.commit()
            params = dict(email=email, token=f'C-{token["token"]}')
            headers = dict(authorization=f'Bearer {SERVER_KEY}')
            request = post(url=EMAIL_URL, params=params, headers=headers)
            return request
        except:
            return except_func('Verification')
    else:
        try:
            query = "SELECT code FROM users WHERE email = %s"
            value = (email,)
            cursor.execute(query, value)
            fetch = cursor.fetchone()
            verify = fetch[0]
            expires = verify.split(':')[1]
            if int(expires) - int(time.time() * 1000) < 0:
                query = 'UPDATE users SET code = %s WHERE email = %s'
                values = ('', email)
                cursor.execute(query, values)
                mydb.commit()
                result = dict(message='Code has expired', status=False)
                return result
            if verify.split(':')[0] == code:
                query = 'UPDATE users SET status = %s WHERE email = %s'
                values = ('verified', email)
                cursor.execute(query, values)
                mydb.commit()
                result = dict(message='Account verified', status=True)
                return result
            else:
                result = dict(message='Invalid code', status=False)
                return result
        except:
            return except_func('Verification')


def db_passcode(uuid: str, passcode: str):
    """
    It takes a uuid and a passcode, hashes the passcode, and updates the database with the hashed
    passcode

    :param uuid: The user's uuid
    :type uuid: str
    :param passcode: str
    :type passcode: str
    :return: A dictionary with a message and a status.
    """
    pass_hash = generate_password_hash(
        password=passcode, method=f"{SALT}", salt_length=57)
    try:
        query = "UPDATE users SET passcode = %s WHERE uuid = %s"
        values = (pass_hash, uuid)
        cursor.execute(query, values)
        mydb.commit()
        return dict(message='Passcode Set', status=True)
    except:
        return except_func('Sign up')


def db_user():
    return


def except_func(error: str):
    """
    It takes a string as an argument and returns a dictionary with a message and a status

    :param error: str
    :type error: str
    :return: A dictionary with two keys: message and status.
    """
    return dict(message=f'{error} system is currently down', status=False)


def db_safe_(magic: str, uuid: str):
    """
    It takes a string and a uuid, and updates the magic_auth column in the users table with the string,
    where the uuid matches the uuid in the table

    :param magic: The magic authentication token
    :type magic: str
    :param uuid: The user's uuid
    :type uuid: str
    :return: A dictionary with the key 'token' and the value of the magic string.
    """
    try:
        query = "UPDATE users SET magic_auth = %s WHERE uuid = %s"
        values = (magic, uuid)
        cursor.execute(query, values)
        mydb.commit()
        return dict(token=magic, status=True)
    except:
        return except_func('Magic authentication')
