import mysql.connector as mc, os
from dotenv import load_dotenv
from werkzeug.security import check_password_hash

load_dotenv()

HOST = os.getenv('HOST')
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')
PORT = os.getenv('PORT')

mydb = mc.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    port=PORT,
    database=DB_NAME
)

cursor = mydb.cursor()


def db_login(email: str, password: str):
    return


def db_onboard():
    return


def db_verify():
    return


def db_passcode():
    return


def db_user():
    return
