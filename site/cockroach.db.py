import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

db_uri = os.getenv("DATABASE_URL")
conn = psycopg2.connect(db_uri)

with conn.cursor() as cur:
    cur.execute("SELECT now()")
    res = cur.fetchall()
    conn.commit()
    print(res)