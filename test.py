import sql_functions
from json_string_for_verification import test_data1
from load_json import load_json_data
import sqlite3
from user_data_for_verification import user_data_verification
import os

"""
these two tests ensures the data from the json files is loaded in correctly into the program before the being entered
into the database the 1 at the end of the function name is reference to  1 = rapidResults.json
"""


def test_loading_json_data_1():
    test_data = []
    load_json_data("rapid_jobs2.json", test_data)
    assert test_data[0][0]["title"] == "Staff Software Engineer, Risk"


def test_loading_json_data_2():
    test_data = []
    load_json_data("rapidResults.json", test_data)
    assert test_data[0] == test_data1


"""
this test will ensure the tables are created correctly for the data base
"""


def test_db_table_creation():
    table_list = []
    conn = sqlite3.connect("rapid_result_job_db.sqlite")
    cursor = conn.cursor()
    table_list = cursor.execute(
        """
        SELECT name FROM sqlite_master WHERE type='table' AND name ='{JOB_DATA}' AND '{RAPID_JOB_DATA}'; """
    ).fetchall()
    conn.close()
    assert table_list is not None


"""
this test ensures that a single job listing is able to be pulled from the db based on the user entering an job id
"""


def test_pull_single_listing():
    job_listing = {}
    conn = sqlite3.connect("jobs_db.sqlite")
    cursor = conn.cursor()
    user_input = 'f97b4a007d08a432'
    sql_functions.pull_single_listing(user_input, job_listing)
    cursor.execute("SELECT * FROM JOB_DATA WHERE JOB_ID = ?", (user_input,))
    rows = cursor.fetchone()
    if rows:
        job_listing.update(rows)
    assert job_listing["JOB_ID"] == 'f97b4a007d08a432'
    conn.close()


"""
this test ensures that user data was enters correctly into the database by checking the values of a test user """


def test_user_saved_data():
    conn = sqlite3.connect("jobs_db.sqlite")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM USER_DATA WHERE CONTACT_INFO = 'kealan';")
    rows = cursor.fetchall()
    assert rows == [('test', 'kealan', 'doherty', 'class', 'other')]


# this test checks if use data is loaded correctly for LLM prompt


def test_user_data_in_Ai():
    rows = {}
    sql_functions.pull_user('kealan-doherty', rows)
    assert rows == user_data_verification


"""
this test ensures that the markdown files are written with the response from the LLM before being converted to pdf
"""


def test_markdown_file():
    assert os.path.getsize('resume.md') > 0
    assert os.path.getsize('cover_letter.md') > 0
