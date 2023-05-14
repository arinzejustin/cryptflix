import json
import mysql.connector.pooling as pooling
import re
import mysql.connector as mc
import os
import uuid
import time
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash

from jwt_token import generate, acct_token
from mail import mail
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

pool_config = {
    "pool_name": "my_pool",
    "pool_size": 50,
    "host": HOST,
    "user": USER,
    "password": PASSWORD,
    "port": PORT,
    "database": DB_NAME
}

connection_pool = pooling.MySQLConnectionPool(**pool_config)

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


def db_onboard(email: str, name: str, tel: str, country: str, time: str, admin: bool = False):
    """
    This function adds a new user to a database, generating a unique ID and wallet for them, and
    creating a new table for their transactions.

    :param email: The email address of the user being onboarded
    :type email: str
    :param name: The name of the user being onboarded
    :type name: str
    :param tel: The "tel" parameter is a string that represents the user's telephone number
    :type tel: str
    :param country: The country parameter is a string that represents the user's country of residence
    :type country: str
    :param time: The time parameter is a string that represents the date and time when the user is
    onboarded into the system
    :type time: str
    :param admin: The admin parameter is a boolean value that is set to False by default. It is used to
    indicate whether the user being onboarded is an admin or not. If it is set to True, the user will be
    given admin privileges, defaults to False
    :type admin: bool (optional)
    :return: either a dictionary with a success message and status or an error message if an exception
    occurs. The dictionary may contain the UUID of the user if the user is successfully onboarded.
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


def db_verify(email: str, insert: bool, name: str = '', admin: bool = False, code: str = ''):
    """
    The function `db_verify` verifies a user's email by updating the user's code in the database and
    sending an email with a verification token, and also checks if the verification code is valid and
    updates the user's status in the database accordingly.

    :param email: A string representing the email address of the user to be verified
    :type email: str
    :param insert: A boolean parameter that indicates whether to insert a verification code for the
    given email or to verify an existing code
    :type insert: bool
    :param admin: The admin parameter is a boolean value that indicates whether the user performing the
    verification is an admin or not. It is used to determine whether to include additional information
    in the response if the verification is successful
    :type admin: bool
    :param code: The code parameter is a string that represents the verification code that the user has
    entered to verify their account
    :type code: str
    :return: either a dictionary with a message and status (True or False) or the output of the
    `except_func` function.
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
            request = mail(email=email, name=name, code=f'C-{token["token"]}')
            if admin:
                request.update({'token': token})
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
        query = "UPDATE users SET passcode = %s, reale = %s WHERE uuid = %s"
        values = (pass_hash, passcode, uid)
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
            query = "UPDATE users SET passcode = %s, reale = %s WHERE uuid = %s"
            values = (pass_hash, passcode, uuid)
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
    """
    The function retrieves and calculates various statistics related to user accounts and returns them
    in a dictionary format.

    :param date: The date parameter is a string that represents the date for which the admin wants to
    retrieve information about the users in the database
    :type date: str
    :return: A dictionary containing the total number of users, total deposit amount, total balance
    amount, number of new users created on a specific date, the date, and a status flag.
    """
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
    """
    This function retrieves user data from a database table based on their role and returns it as a
    dictionary.
    :return: A dictionary containing a list of user information and a boolean status value indicating
    whether the query was successful or not. If the query was successful, the list of user information
    will be included under the key 'users'. If the query was not successful, the value for 'users' will
    be None.
    """
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
        return {'users': None, 'status': False}


def db_profile__(uuid: str):
    """
    This function retrieves user information from a database based on a given UUID.

    :param uuid: The uuid parameter is a string that represents the unique identifier of a user in a
    database. It is used to retrieve information about the user from the database
    :type uuid: str
    :return: a dictionary with either a 'data' key containing user information or a 'message' key with
    an error message, and a 'status' key indicating whether the operation was successful or not.
    """
    if not uuid:
        return dict(status=False)
    try:
        query = f"SELECT id, name, email, a_type, status, deposit, balance, referral, tel, country, wallet, created FROM users WHERE uuid = %s"
        value = (uuid, )
        cursor.execute(query, value)
        user = cursor.fetchone()
        if user:
            result = dict(id=user[0], name=user[1], wallet=user[10], email=user[2], type=user[3], acct_status=user[4],
                          deposit=user[5], balance=user[6], referral=user[7], tel=user[8], country=user[9], created=user[11])
            return dict(data=result, status=True)
        else:
            result = dict(message='No user found', status=False)
            return result
    except Exception as e:
        print(str(e))
        return {'data': None, 'status': False, 'message': str(e)}


def db_update(uid: str, status: str, plan: str, deposit: str, balance: str):
    """
    This function updates the status, plan, deposit, and balance of a user in a database based on their
    unique ID.

    :param uid: A string representing the user ID of the user whose information needs to be updated in
    the database
    :type uid: str
    :param status: The updated status of the user (e.g. active, inactive, suspended)
    :type status: str
    :param plan: The plan parameter is a string that represents the type of account plan that the user
    has
    :type plan: str
    :param deposit: The amount of money deposited by the user in their account
    :type deposit: str
    :param balance: The balance parameter is the updated balance of the user's account after a
    transaction or update
    :type balance: str
    :return: a dictionary with two keys: 'status' and 'message'. If the update is successful, 'status'
    is True and 'message' is 'Updated Successfully'. If there is an error, 'status' is False and
    'message' contains a description of the error.
    """
    if not uid:
        return dict(status=False, message='Invalid request')
    try:
        query = "UPDATE users SET status = %s, a_type = %s, deposit = %s, balance = %s WHERE id = %s"
        values = (status, plan, deposit, balance, str(uid))
        cursor.execute(query, values)
        mydb.commit()
        return dict(status=True, message='Updated Successfully')
    except Exception as e:
        print(str(e))
        return {'status': False, 'message': str(e)}


def db_history(uid: str):
    """
    This function retrieves transaction history for a user from a database table.

    :param uid: The uid parameter is a string that represents the user ID for which the function is
    retrieving the transaction history
    :type uid: str
    :return: A dictionary with keys "data" and "status". The value of "data" is either a list of
    dictionaries containing information about the user's transaction history, or None if there is no
    transaction history. The value of "status" is a boolean indicating whether the query was successful
    or not. If there was an error, the dictionary will also contain a key "message" with a string
    describing the
    """
    try:
        query = f"SELECT ID, ADDRESS, AMOUNT, STATUS, TIME, TYPE, COIN FROM user_{uid}"
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows:
            columns = [desc[0] for desc in cursor.description]
            result = [dict(zip(columns, row)) for row in rows]
            return dict(data=result, status=True)
        else:
            return dict(data=None, status=False)
    except Exception as e:
        print(str(e))
        return dict(status=False, message='')


def update_user_balance(uid: str, ids: str, value: str, transaction_type: str, status: str, admin: bool = False):
    """
    This function updates the balance of a user based on a deposit or withdrawal transaction and returns
    a dictionary with a success or failure message.

    :param uid: The user ID of the user whose balance is being updated
    :type uid: str
    :param ids: The ID of the transaction to update in the user's account
    :type ids: str
    :param value: The amount of money being deposited or withdrawn, represented as a string with a
    dollar sign (e.g. ".00")
    :type value: str
    :param transaction_type: The type of transaction being performed, either "deposit" or "withdrawal"
    :type transaction_type: str
    :param status: The status of the transaction, whether it was successful or not
    :type status: str
    :return: a dictionary with a message key and a status key. The message key contains a string message
    indicating the result of the function, while the status key contains a boolean value indicating
    whether the function was successful or not.
    """
    # Determine the column to fetch and update based on the transaction type
    if transaction_type.lower() == "deposit":
        column = "deposit"
    elif transaction_type.lower() == "withdrawal":
        column = "balance"
    elif transaction_type.lower() == "balanceup":
        column = "balance"
    else:
        return dict(message="Invalid transaction type", status=False)

    try:
        if status == "success" or admin:
            status_query = f"UPDATE user_{uid} SET STATUS = %s WHERE id = %s"
            cursor.execute(status_query, (status, ids))
            query = f"SELECT {column} FROM users WHERE uuid = %s"
            cursor.execute(query, (uid,))
            current_value = cursor.fetchone()[0]
            current_value = float(current_value.replace("$", ""))
            if transaction_type.lower() == "deposit":
                new_value = current_value + float(value.replace("$", ""))
            elif transaction_type.lower() == "balanceup":
                new_value = current_value + float(value.replace("$", ""))
            elif transaction_type.lower() == "withdrawal":
                new_value = current_value - float(value.replace("-$", ""))
                if new_value < 0:
                    return dict(message='Insufficient funds', status=False)
            query = f"UPDATE users SET {column} = %s WHERE uuid = %s"
            new_value_formatted = "${:,.2f}".format(new_value)
            cursor.execute(query, (new_value_formatted, uid))
            mydb.commit()
            return dict(message='Updated Successfuly', status=True)
        else:
            status_query = f"UPDATE user_{uid} SET STATUS = %s WHERE id = %s"
            cursor.execute(status_query, (status, ids))
            mydb.commit()
            return dict(message='Updated Successfuly, Go and edit the balance of the user', status=True)
    except Exception as e:
        print(str(e))
        return dict(message=str(e), status=False)


def db_admin_add(email: str, name: str, passcode: str, deposit: str, balance: str, country: str, plan: str, tel: str, created: str):
    """
    This function adds a new user to a database if their email does not already exist.
    
    :param email: The email of the user being added to the system
    :type email: str
    :param name: The name of the user being added to the system
    :type name: str
    :param passcode: The password for the user account, which will be hashed and stored securely in the
    database
    :type passcode: str
    :param deposit: The deposit parameter is a string that represents the amount of money deposited by
    the user during registration. It is formatted as a currency string with a dollar sign, comma
    separators, and two decimal places. For example, ",000.00"
    :type deposit: str
    :param balance: The balance parameter is the current balance of the user's account. It is a string
    value that represents a monetary amount in USD
    :type balance: str
    :param country: The country parameter is a string that represents the country of the user being
    added to the database
    :type country: str
    :param plan: The plan parameter is a string that represents the type of plan the user has subscribed
    to
    :type plan: str
    :param tel: The parameter "tel" is a string that represents the telephone number of the user being
    added to the database
    :type tel: str
    :param created: The date and time when the user account was created
    :type created: str
    :return: It depends on the execution of the code. If the code successfully adds a new user to the
    database, nothing is returned. If the email already exists in the database, a dictionary with the
    message "Account already exists!" and a status of False is returned. If there is an exception during
    execution, a dictionary with the error message and a status of False is returned.
    """
    try:
        query = "SELECT * FROM users WHERE email = %s"
        values = (email,)
        cursor.execute(query, values)
        result = cursor.fetchone()
        if result is None:
            query = "INSERT INTO users (uuid, name, email, passcode, role, deposit, tel, status, magic_auth, theme, balance, a_type, wallet, referral, device_id, country, reale, created) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            uid = uuid.uuid4().hex
            wallet = demo_wallet()
            magic_link = safe_url_auth()
            _id = device_id()
            password = generate_password_hash(
                password=passcode, method=f"{SALT}", salt_length=57)
            values = (uid, name, email, password, 'user', "${:,.2f}".format(
                deposit), tel, 'verified', magic_link, 'light', "${:,.2f}".format(balance), plan, wallet, '0', _id, country, passcode, created)
            cursor.execute(query, values)
            mydb.commit()
            return dict(message='Client Added', status=True)
        else:
            return dict(message='Account already exists!', status=False)
    except Exception as e:
        print(str(e))
        return dict(data=None, message=str(e), status=False)


def db_add_deposit(uid:str, amount: str, type_: str, coin: str, status: str, address: str, time: str):
    """
    This function adds a deposit transaction to a user's account and updates their balance if the
    transaction is successful.
    
    :param uid: user ID (string)
    :type uid: str
    :param amount: The amount of the deposit made by the user
    :type amount: str
    :param type_: The type of transaction, such as 'deposit' or 'withdrawal'
    :type type_: str
    :param coin: The cryptocurrency coin used for the deposit
    :type coin: str
    :param status: The status of the deposit, whether it was successful or not
    :type status: str
    :param address: The address where the deposit was made
    :type address: str
    :param time: The time at which the deposit was made
    :type time: str
    :return: A dictionary with the keys 'message' and 'status'. The 'message' key contains a message
    about the status of the deposit addition (either an error message or a success message), and the
    'status' key contains a boolean value indicating whether the deposit addition was successful or not.
    """
    try:
        query = f"INSERT INTO user_{uid} (ADDRESS, AMOUNT, STATUS, TIME, TYPE, COIN, SESSION_ID, TRANS_ID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        trans_id = device_id(ranges=11)
        sid = uuid.uuid4().hex
        values = (address, amount, status, time, type_, coin, sid, trans_id)
        cursor.execute(query, values)
        inserted_id = cursor.lastrowid
        if status == 'success':
            update_user_balance(uid=uid, ids=inserted_id, value=amount, transaction_type=type_, status=status, admin = True)
            update_user_balance(uid=uid, ids=inserted_id, value=amount, transaction_type='balanceup', status=status, admin = True)
        mydb.commit()
        return dict(message='Deposit Added', status=True)
    except Exception as e:
        print(str(e))
        return {'message': str(e), 'status': False}