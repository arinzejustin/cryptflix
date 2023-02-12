import mysql.connector as mc
import os, uuid
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash

from jwt_token import generate
from netrequest import post

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
            print(password, user[5])
            verify = check_password_hash(user[5], password)
            if verify:
                token = generate(uuid=user[1], email=email, key=user[0], name=user[2])
                result = dict(message='Login Successful', status=True, uuid=user[1], name=user[2], email=email,
                              bearer=token)
                return result
            else:
                result = dict(message='Invalid Credentials', status=False, link=2)
                return result
        else:
            result = dict(message='User Not Found', status=False)
            return result
    except:
        return except_func('Login')


def db_onboard():
    return


def db_verify(email: str, code: str, insert: bool):
    """
    It takes in an email, a code, and a boolean value. If the boolean value is true, it inserts the code
    into the database and sends an email to the user. If the boolean value is false, it checks if the
    code in the database matches the code passed in. If it does, it returns a message saying the account
    is verified. If it doesn't, it returns a message saying the code is invalid.
    
    :param email: str
    :type email: str
    :param code: str = The code that is sent to the user's email
    :type code: str
    :param insert: bool
    :type insert: bool
    :return: A dictionary with the keys 'message' and 'status'
    """
    if insert:
        try:
            query = "UPDATE users SET code = %s WHERE email = %s"
            value = (code, email)
            cursor.execute(query, value)
            mydb.commit()
            params = dict(email=email)
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
            if fetch[0] == code:
                result = dict(message='Account Verified', status=True)
                return result
            else:
                result = dict(message='Invalid Code', status=False)
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
    pass_hash = generate_password_hash(password=passcode, method=f"{SALT}", salt_length=57)
    try:
        query = "UPDATE users SET passcode = %s WHERE uuid = %s"
        value = (pass_hash, uuid)
        cursor.execute(query, value)
        mydb.commit()
        return dict(message='Passcode Set', status=True)
    except:
        return except_func('Sign Up')


def db_user():
    return


def except_func(error: str):
    """
    It takes a string as an argument and returns a dictionary with a message and a status
    
    :param error: str
    :type error: str
    :return: A dictionary with two keys: message and status.
    """
    return dict(message=f'{error} System Is Currently Down', status=False)
