from test_data import test_data1
from load_json import load_json_data
import sqlite3


"""
these two tests ensures the data from the json files is loaded in correctly into the program before the being entered
into the database the 1 at the end of the function name is reference to  1 = rapidResults.json
"""


def test_loading_json_data_1():
    test_data = []
    load_json_data('rapid_jobs2.json', test_data)
    assert test_data[0][0]['title'] == 'Staff Software Engineer, Risk'


def test_loading_json_data_2():
    test_data = []
    load_json_data('rapidResults.json', test_data)
    assert test_data[0] == test_data1


"""
this test will ensure the tables are created correctly for the data base
"""


def test_db_table_creation():
    table_list = []
    conn = sqlite3.connect('rapid_result_job_db.sqlite')
    cursor = conn.cursor()
    table_list = cursor.execute('''
        SELECT name FROM sqlite_master WHERE type='table' AND name ='{JOB_DATA}' AND '{RAPID_JOB_DATA}'; ''').fetchall()
    conn.close()
    assert table_list is not None
