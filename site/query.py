import mysql.connector as mc
import os
import uuid
import time
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash

from jwt_token import generate, acct_token
from netrequest import post, get
from wallet import demo_wallet, device_id, safe_url_auth

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
                ssid = uuid.uuid4().hex
                token = generate(
                    uuid=user[1], email=email, key=user[0], name=user[2], ssid=ssid)
                result = dict(message='Login successful', status=True, uuid=user[1], account=user[8], name=user[2], email=email,
                              bearer=token, role=user[5] or 'user', maogic=user[9], ssid=ssid)
                return result
            else:
                result = dict(message='Invalid credentials',
                              status=False, link=2)
                return result
        else:
            result = dict(message='User not found', status=False)
            return result
    except Exception as e:
        print(str(e))
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
        print(account)
        if account:
            if account[4] is None:
                query = "DELETE FROM users WHERE email = %s"
                query2 = f"DROP TABLE IF EXISTS user_{account[1]}"
                value = (email, )
                cursor.execute(query, value)
                cursor.execute(query2)
                mydb.commit()
                return db_onboard(email=account[3], name=name, tel=tel)
            return dict(message='Account already exists!', status=False)
        query = 'INSERT INTO users (uuid, name, email, tel, a_type, wallet, theme, balance, magic_auth, referral, device_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        uid = uuid.uuid4().hex
        wallet = demo_wallet()
        magic_link = safe_url_auth()
        _id = device_id()
        values = (uid, name, email, tel, 'Plan 1', wallet, 'light', '$50.00', magic_link, '0', _id)
        cursor.execute(query, values)
        mydb.commit()
        onboard = db_verify(email=email, insert=True)
        if onboard['status']:
            try:
                cursor.execute(
                    f'CREATE TABLE user_{uid} (ID INT AUTO_INCREMENT PRIMARY KEY, ADDRESS VARCHAR(255), TRANSACTION VARCHAR(100), STATUS VARCHAR(100), TIME VARCHAR(100), TRANS_PASS VARCHAR(100))')
                mydb.commit()
                onboard.update({'uuid': uid})
            except Exception as e:
                query = "DELETE FROM users WHERE uuid = %s"
                query2 = f"DROP TABLE IF EXISTS user_{uid}"
                value = (uid, )
                cursor.execute(query, value)
                cursor.execute(query2)
                mydb.commit()
                print(str(e))
                return except_func('Accounts')
        else:
            query = "DELETE FROM users WHERE uuid = %s"
            value = (uid, )
            cursor.execute(query, value)
            mydb.commit()
        return onboard
    except Exception as e:
        mydb.rollback()
        query = "DELETE FROM users WHERE email = %s"
        value = (email, )
        cursor.execute(query, value)
        mydb.commit()
        print(str(e))
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
            mydb.rollback()
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
        except Exception as e:
            mydb.rollback()
            print(str(e))
            return except_func('Verification')


def db_passcode(uid: str, passcode: str):
    """
    It takes a uid and a passcode, hashes the passcode, and updates the database with the hashed
    passcode

    :param uid: The user's uid
    :type uid: str
    :param passcode: str
    :type passcode: str
    :return: A dictionary with a message and a status.
    """
    pass_hash = generate_password_hash(
        password=passcode, method=f"{SALT}", salt_length=57)
    try:
        query = "UPDATE users SET passcode = %s WHERE uuid = %s"
        values = (pass_hash, uid)
        cursor.execute(query, values)
        cursor.execute('SELECT * FROM users WHERE uuid = %s', (uid,))
        user = cursor.fetchone()
        ssid = uuid.uuid4().hex
        token = generate(
            uuid=uid, email=user[3], key=user[0], name=user[2], ssid=ssid)
        mydb.commit()
        return dict(message='Passcode Set', status=True, uuid=user[1], account=user[8], name=user[2], email=user[3],
                    bearer=token, role=user[5] or 'user', maogic=user[9], ssid=ssid)
    except Exception as e:
        mydb.rollback()
        print(str(e))
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
    if not uuid or uuid is None:
        return dict(token=None, status=False)
    try:
        query = "UPDATE users SET magic_auth = %s WHERE uuid = %s"
        values = (magic, uuid)
        cursor.execute(query, values)
        mydb.commit()
        return dict(token=magic, status=True)
    except Exception as e:
        mydb.rollback()
        print(str(e))
        return except_func('Magic authentication')
