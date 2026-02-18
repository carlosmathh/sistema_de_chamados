import os
import pymysql
from dotenv import load_dotenv
from pymysql.connections import Connection

load_dotenv()


def get_connection() -> Connection:

    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),  # type: ignore
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),  # type: ignore
        database=os.getenv("DB_NAME"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )
