import sqlite3
from typing import Tuple


def open_database(
    filename: str,
) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:  # opens database
    db_connection = sqlite3.connect(filename)
    cursor = db_connection.cursor()
    return db_connection, cursor


def close_database(connection: sqlite3.Connection):  # closes database
    connection.commit()
    connection.close()


def set_rapid_db(cursor: sqlite3.Cursor):
    table = """CREATE TABLE IF NOT EXISTS JOB_DATA(JOB_ID TEXT PRIMARY KEY, JOB_TITLE TEXT , JOB_COMPANY TEXT, JOB_DESCR
            IPTION TEXT, JOB_IMAGE TEXT, JOB_LOCATION TEXT, JOB_EMPLOYMENT TEXT, JOB_DATE_POSTED TEXT, JOB_SALARY INT,JO
            B_PROVIDER TEXT);"""
    cursor.execute(table)


def set_results_db(cursor: sqlite3.Cursor):
    table = """
    CREATE TABLE IF NOT EXISTS RAPID_JOB_DATA (
        JOB_ID TEXT PRIMARY KEY,
        JOB_SITE TEXT,
        JOB_URL TEXT,
        JOB_TITLE TEXT,
        JOB_COMPANY TEXT,
        JOB_LOCATION TEXT,
        JOB_TYPE TEXT,
        JOB_DATE_POSTED TEXT,
        JOB_SALARY_INTERVAL TEXT,
        JOB_SALARY_MIN INT,
        JOB_SALARY_MAX INT,
        JOB_IS_REMOTE TEXT,
        JOB_EMAILS TEXT,
        JOB_DESCRIPTION TEXT
    );
    """
    cursor.execute(table)
