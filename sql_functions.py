import sqlite3
from typing import Tuple

"""
this code has the functions used for the database created for this project from opening,closing,creating tables, loading
data into the tables, and pulling data from the database
"""


def open_database(filename: str, ) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:  # opens database
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


def pull_data_rapid2(input_text: str, pulled_jobs: list):
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


def pull_single_listing(input_text2: str, job_listing: dict):
    conn = sqlite3.connect('jobs_db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""SELECT *  FROM JOB_DATA WHERE JOB_ID = ? """, (input_text2,))
    rows = cursor.fetchone()
    if rows:
        job_listing.update(rows)

    cursor.execute("""SELECT *  FROM RAPID_JOB_DATA WHERE JOB_ID = ? """, (input_text2,))
    rows2 = cursor.fetchone()
    if rows2:
        job_listing.update(rows2)

    print(job_listing)
    return job_listing


def create_user_db():
    conn = sqlite3.connect('jobs_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS USER_DATA (
         USERNAME TEXT PRIMARY KEY,
         CONTACT_INFO TEXT,
         PROJECT TEXT,
         CLASSES TEXT,
         OTHER TEXT
         );
    """)
    conn.commit()
    conn.close()


def load_user_db(username: str, contact_info: str, project_info: str, classes_info: str, other_info: str):
    conn = sqlite3.connect('jobs_db.sqlite')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO USER_DATA(USERNAME, CONTACT_INFO, PROJECT, CLASSES, OTHER) VALUES (?, ?, ?, ?, ?)""",
                   [username, contact_info, project_info, classes_info, other_info])
    conn.commit()
    conn.close()


def pull_user(username: str, user_data: dict):
    conn = sqlite3.connect('jobs_db.sqlite')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""SELECT *  FROM USER_DATA WHERE USERNAME = ? """, (username,))
    rows = cursor.fetchone()
    if rows:
        user_data.update(rows)
    return user_data


def upload_data1(
        data: list, cursor
):  # this functions adds data from rapid_jobs2 to the database
    x = 0
    sorted_data = {}
    import_data = {}
    conn, cursor = open_database("jobs_db.sqlite")
    for row in data:
        sorted_data = data[x]
        import_data = sorted_data[0]
        cursor.execute(
            """INSERT OR IGNORE INTO JOB_DATA (JOB_ID, JOB_TITLE, JOB_COMPANY, JOB_DESCRIPTION, JOB_IMAGE
                           , JOB_LOCATION, JOB_EMPLOYMENT, JOB_DATE_POSTED, JOB_SALARY) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                import_data["id"],
                import_data["title"],
                import_data["company"],
                import_data["description"],
                import_data["image"],
                import_data["location"],
                import_data["employmentType"],
                import_data["datePosted"],
                import_data["salaryRange"],
            ],
        )
        x += 1
    conn.commit()
    conn.close()


def upload_data2(
        data: list, cursor
):  # this function adds the data from rapidResults.json to database
    x = 0
    sorted_data = {}
    conn, cursor = open_database("jobs_db.sqlite")
    set_results_db(cursor)
    for row in data:
        sorted_data = data[x]
        cursor.execute(
            """INSERT OR IGNORE INTO RAPID_JOB_DATA (JOB_ID, JOB_SITE, JOB_URL, JOB_TITLE, JOB_COMPANY, JOB_LOCATION
            , JOB_TYPE, JOB_DATE_POSTED, JOB_SALARY_INTERVAL, JOB_SALARY_MIN, JOB_SALARY_MAX, JOB_IS_REMOTE
            ,JOB_EMAILS,JOB_DESCRIPTION) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                sorted_data["id"],
                sorted_data["site"],
                sorted_data["job_url"],
                sorted_data["title"],
                sorted_data["company"],
                sorted_data["location"],
                sorted_data["job_type"],
                sorted_data["date_posted"],
                sorted_data["interval"],
                sorted_data["min_amount"],
                sorted_data["max_amount"],
                sorted_data["is_remote"],
                sorted_data["emails"],
                sorted_data["description"],
            ],
        )
        x += 1
    conn.commit()
    conn.close()
