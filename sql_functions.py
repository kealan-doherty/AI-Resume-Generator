import sqlite3
from typing import Tuple


def open_database(filename: str,) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:  # opens database
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

    #  this function will pull jobs based on the job title provided buy the user from 1st database
def pull_data_rapid2(input_text:str, pulled_jobs:list):
    conn = sqlite3.connect('jobs_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("""SELECT JOB_ID, JOB_TITLE, JOB_COMPANY, JOB_LOCATION FROM JOB_DATA WHERE JOB_TITLE LIKE ?""",
                   (input_text,))
    rows = cursor.fetchall()
    for row in rows:
        pulled_jobs.append(row)

    cursor.execute("""SELECT JOB_ID, JOB_SITE, JOB_TITLE, JOB_COMPANY, JOB_LOCATION FROM RAPID_JOB_DATA WHERE
    JOB_TITLE LIKE ?""", (input_text,))
    rapid_data = cursor.fetchall()
    for row in rapid_data:
        pulled_jobs.append(row)

    return pulled_jobs

def pull_single_listing(input_text2:str, job_listing:list):
    conn = sqlite3.connect('jobs_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("""SELECT *  FROM JOB_DATA WHERE JOB_ID = ? """,(input_text2, ))
    rows = cursor.fetchall()
    for row in rows:
        job_listing.append(row)

    cursor.execute("""SELECT *  FROM RAPID_JOB_DATA WHERE JOB_ID = ? """, (input_text2,))
    rows = cursor.fetchall()
    for row in rows:
        job_listing.append(row)

    return job_listing


def create_user_db():
    conn = sqlite3.connect('jobs_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS USER_DATA (
         CONTACT_INFO TEXT PRIMARY KEY,
         PROJECT TEXT,
         CLASSES TEXT,
         OTHER TEXT
         );
    """)
    conn.commit()
    conn.close()


def load_user_db(contact_info:str, project_info:str, classes_info:str, other_info:str):
    conn = sqlite3.connect('jobs_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO USER_DATA(CONTACT_INFO, PROJECT, CLASSES, OTHER) VALUES (?, ?, ?, ?)""",
                   [contact_info, project_info, classes_info, other_info])
    conn.commit()
    conn.close()