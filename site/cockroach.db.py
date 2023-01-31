import mysql.connector, pymongo, os
from dotenv import load_dotenv

load_dotenv()

DB_URI = os.getenv('DB_URI')

client = pymongo.MongoClient(DB_URI)

dblist = client.list_database_names()
for v in dblist:
    print(v)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password=""
)

cursor = mydb.cursor()

cursor.execute("SHOW DATABASES")

for x in cursor:
    if x == 'test':
        break
    print(x)
