import json
import sqlite3


def load_json_data1(filename,data:list):
    with open(filename, 'r') as file:
        for line in file:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError as e:
                print("error decoding")
    return data


def load_json_data2(filename,data_2:dict):
    with open(filename, 'r') as file:
        for line in file:
            try:
                data_2 = json.loads(line)
            except json.JSONDecodeError as e:
                print("error decoding")
    return data_2


def set_rapid_db(cursor: sqlite3.Cursor):
    table = '''CREATE TABLE JOB_DATA(
                JOB_ID TEXT PRIMARY KEY, 
                JOB_TITLE TEXT ,
                JOB_COMPANY TEXT,
                JOB_DESCRIPTION TEXT,
                JOB_IMAGE TEXT,
                JOB_LOCATION TEXT,
                JOB_EMPLOYMENT TEXT,
                JOB_DATE_POSTED TEXT,
                JOB_SALARY INT,
                JOB_PROVIDER TEXT);'''
    cursor.execute(table)

def set_results_db(cursor: sqlite3.Cursor):
    table = '''CREATE TABLE RAPID_JOB_DATA(
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
              JOB_DESCRIPTION TEXT);'''
    cursor.execute(table)


