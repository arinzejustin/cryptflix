import json
import re
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
                result = dict(message='Login successful', status=True, uuid=user[1], account=user[9], name=user[2], email=email,
                              bearer=token, role=user[5], maogic=user[10], ssid=ssid)
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


def db_onboard(email: str, name: str, tel: str, country: str, time: str):
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
                query = "DELETE FROM users WHERE email = %s"
                query2 = f"DROP TABLE IF EXISTS user_{account[1]}"
                value = (email, )
                cursor.execute(query, value)
                cursor.execute(query2)
                mydb.commit()
                return db_onboard(email=account[3], name=name, tel=tel)
            return dict(message='Account already exists!', status=False)
        query = 'INSERT INTO users (uuid, name, email, tel, role, a_type, wallet, theme, balance, magic_auth, referral, device_id, deposit, country, created) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        uid = uuid.uuid4().hex
        wallet = demo_wallet()
        magic_link = safe_url_auth()
        _id = device_id()
        values = (uid, name, email, tel, 'user', 'Plan 1', wallet, 'light',
                  '$50.00', magic_link, '0', _id, '$50.00', country, time)
        cursor.execute(query, values)
        mydb.commit()
        onboard = db_verify(email=email, insert=True)
        if onboard['status']:
            try:
                cursor.execute(
                    f'CREATE TABLE user_{uid} (ID INT AUTO_INCREMENT PRIMARY KEY, ADDRESS VARCHAR(255), AMOUNT VARCHAR(100), STATUS VARCHAR(100), TIME VARCHAR(100), TYPE VARCHAR(100), COIN VARCHAR(100), SESSION_ID VARCHAR(100), TRANS_ID VARCHAR(100))')
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
        return dict(message='Passcode Set', status=True, uuid=user[1], account=user[9], name=user[2], email=user[3],
                    bearer=token, role=user[5], maogic=user[10], ssid=ssid)
    except Exception as e:
        mydb.rollback()
        print(str(e))
        return except_func('Sign up')


def db_trans(uuid: str):
    """
    This function retrieves data from a MySQL database table for a specific user UUID and returns it as
    a dictionary with a status flag.

    :param uuid: The uuid parameter is a string that represents a unique identifier for a user. It is
    used to query a specific table in a database that contains information about that user
    :type uuid: str
    :return: A dictionary with two keys: 'data' and 'status'. The value of 'data' is either a list of
    dictionaries containing the results of a SELECT query on a database table, or None if there are no
    results or an error occurred. The value of 'status' is a boolean indicating whether the query was
    successful (True) or not (False).
    """
    if not uuid:
        return {'data': None, 'status': False}
    try:
        query = f"SELECT * FROM user_{uuid}"
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows:
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            return {'data': result, 'status': True}
        else:
            return {'data': None, 'status': False}
    except Exception as e:
        print(f"An error occurred: {e}")
        mydb.rollback()
        return {'data': None, 'status': False}


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


def db_password__(uuid: str, update: bool, passcode: str):
    """
    This is a Python function that updates or verifies a user's password in a database using hashed
    passwords.

    :param uuid: A string representing the unique identifier of a user in a database
    :type uuid: str
    :param update: A boolean value indicating whether to update the password or not
    :type update: bool
    :param passcode: The passcode parameter is a string that represents the password that the user wants
    to set or verify
    :type passcode: str
    :return: a dictionary with different key-value pairs depending on the input parameters and the
    execution of the code. The keys in the dictionary can be 'token', 'status', 'message', and 'reload'.
    The values for these keys can be None, True, False, or a string message.
    """
    if not uuid or uuid is None:
        return dict(token=None, status=False)
    if update:
        if len(passcode) < 8:
            return dict(status=False, message='Passcode is too short')
        try:
            pass_hash = generate_password_hash(
                password=passcode, method=f"{SALT}", salt_length=57)
            query = "UPDATE users SET passcode = %s WHERE uuid = %s"
            values = (pass_hash, uuid)
            cursor.execute(query, values)
            mydb.commit()
            return dict(message="Passcode updated successfully", status=True)
        except Exception as e:
            mydb.roolback()
            print(str(e))
            return except_func('Password update')
    else:
        try:
            query = "SELECT passcode FROM users WHERE uuid = %s"
            value = (uuid, )
            cursor.execute(query, value)
            user = cursor.fetchone()
            if user:
                verify = check_password_hash(user[0], passcode)
                if verify:
                    return dict(status=True)
                else:
                    return dict(status=False, message='Incorrect passcode')
            else:
                return dict(status=False, reload=True, message='Incorrect passcode')
        except Exception as e:
            print(str(e))
            return except_func('Passcode ')


def fetch_user(uuid: str):
    """
    The function fetches user data from a database based on a given UUID and returns a dictionary with
    the user's information or an error message.

    :param uuid: The uuid parameter is a string that represents the unique identifier of a user. It is
    used to fetch the user's information from a database
    :type uuid: str
    :return: a dictionary with information about a user, including their name, telephone number, account
    status, UUID, email, magic, balance, account, wallet, device ID, referral, and status. If the UUID
    is invalid or the user is not found, a different dictionary with a status of False and an
    appropriate message is returned.
    """
    if not uuid:
        return dict(status=False, message="Invalid User")
    try:
        query = 'SELECT * FROM users WHERE uuid = %s'
        value = (uuid, )
        cursor.execute(query, value)
        user = cursor.fetchone()
        if user:
            result = dict(name=user[2], tel=user[7], acc_status=user[9], uuid=user[1], email=user[3], magic=user[10], balance=user[12],
                          account=user[13], wallet=user[14], device_id=user[16], referral=user[15], deposit=user[6], country=user[17], created=user[18], status=True)
            return result
        else:
            return dict(status=False, message='User not found')
    except Exception as e:
        print(str(e))
        return except_func('User')


def add(amount: str, status: str, time: any, coin: str, address: str, type_: str, uuid: str, session: str):
    """
    The function adds transaction details to a user's database table and returns a success message or an
    error message.

    :param amount: The amount of the transaction as a string
    :type amount: str
    :param status: The status of the transaction (e.g. "pending", "completed", "failed")
    :type status: str
    :param time: The time parameter is of type 'any', which means it can accept any data type. However,
    based on its usage in the code, it is expected to be a timestamp indicating the time of the
    transaction
    :type time: any
    :param coin: The type of cryptocurrency being transacted (e.g. Bitcoin, Ethereum, Litecoin, etc.)
    :type coin: str
    :param address: The address of the recipient of the transaction
    :type address: str
    :param type_: The type of transaction being performed (e.g. deposit, withdrawal, transfer)
    :type type_: str
    :param uuid: The uuid parameter is a unique identifier for a user. It is used to identify the
    specific user's table in the database where their transaction information will be stored
    :type uuid: str
    :param session: The session parameter is a string that represents the session ID of the user who
    initiated the transaction. It is used to identify the user and link the transaction to their account
    :type session: str
    :return: a dictionary with the message 'Your transaction is being processed' and a status of True if
    the try block is successfully executed. If there is an exception, the function returns the output of
    the except_func('Transaction') function.
    """
    try:
        trans_id = device_id(ranges=11)
        query = f"INSERT INTO user_{uuid} (ADDRESS, AMOUNT, STATUS, TIME, TYPE, COIN, SESSION_ID, TRANS_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (address, amount, status, time,
                  type_, coin, session, str(trans_id))
        cursor.execute(query, values)
        mydb.commit()
        return dict(message='Your transaction is being processed', status=True)
    except Exception as e:
        mydb.rollback()
        print(str(e))
    return except_func('Transaction')


def db_ref(user: str):
    """
    The function updates the referral count of a user in a database based on their device ID.
    
    :param user: The user parameter is a string representing the device ID of a user
    :type user: str
    :return: A dictionary with a "status" key indicating whether the function was successful or not. If
    successful, the value of "status" is True, otherwise it is False.
    """
    if not user:
        return dict(status=False)
    try:
        query = "SELECT referral FROM users WHERE device_id = %s"
        value = (user, )
        cursor.execute(query, value)
        users = cursor.fetchone()
        if users:
            refers = int(users[0])
            newref = refers + 1
            try:
                query = "UPDATE users SET referral = %s WHERE device_id = %s"
                values = (str(newref), user)
                cursor.execute(query, values)
                mydb.commit()
                return dict(status=True)
            except Exception as e:
                mydb.rollback()
                print(str(e))
                return dict(status=False)
    except Exception as e:
        mydb.rollback()
        print(str(e))
        return dict(status=False)

def db_admin__(date: str):
    try:
        query = "SELECT COUNT(*) FROM users"
        cursor.execute(query)
        result = cursor.fetchone()
        count = result[0]
        query_deposit = "SELECT deposit FROM users"
        cursor.execute(query_deposit)
        rows_deposit = cursor.fetchall()
        sum_depsoit = 0
        for row in rows_deposit:
            amount = re.sub('[^\d.]', '', row[0])
            sum_depsoit += float(amount)
        query2 = "SELECT COUNT(*) FROM users WHERE created LIKE %s"
        cursor.execute(query2, (f"%{date}%",))
        counts = cursor.fetchone()[0]
        query_balance = "SELECT deposit FROM users"
        cursor.execute(query_balance)
        rows_balance = cursor.fetchall()
        sum_balance = 0
        for row in rows_balance:
            amount = re.sub('[^\d.]', '', row[0])
            sum_balance += float(amount)
        return dict(user=count, deposit=f"${sum_depsoit}0", balance=f"${sum_balance}0", newUser=counts, date=date, status=True)
    except Exception as e:
        print(str(e))
        return except_func('Admin request')


def db_users__():
    try:
        query = f"SELECT id, name, email, a_type, uuid, country FROM users WHERE role = %s"
        value = ('user', )
        cursor.execute(query, value)
        rows = cursor.fetchall()
        if rows:
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            return {'users': result, 'status': True}
        else:
            return {'users': None, 'status': False}
    except Exception as e:
        print(f"An error occurred: {e}")
        mydb.rollback()
        return {'data': None, 'status': False}