import load_JSON
import private
import google.generativeai as genai
import sqlite3
from typing import Tuple


def open_database(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)
    cursor = db_connection.cursor()
    return db_connection, cursor


def close_database(connection: sqlite3.Connection):
    connection.commit()
    connection.close()

def upload_data(data:list, cursor):
    x=0
    sorted_data = []
    conn,cursor = open_database('jobs_db.sqlite')
    for row in data:
        sorted_data = data[x]
        cursor.executemany('''INSERT INTO JOB_DATA (JOB_ID, JOB_TITLE, JOB_COMPANY, JOB_DESCRIPTION, JOB_IMAGE,
             JOB_LOCATION, JOB_EMPLOYMENT, JOB_DATE_POSTED, JOB_SALARY, JOB_PROVIDER)VALUES (?, ?, ?, ?,
              ?, ?, ?, ?, ?, ?)''', sorted_data)
        x+=1
    conn.commit()
    conn.close()


def main():
    data = []
    load_JSON.load_json_data('rapid_jobs2.json', data) # loads JSON from file
    conn, cursor = open_database('jobs_db.sqlite') # opens database
    upload_data(data, cursor)
    genai.configure(api_key=private.API_KEY)  # Import API key
    # Create the model

    generation_config = {
      "temperature": 1,
      "top_p": 0.95,
      "top_k": 40,
      "max_output_tokens": 8192,
      "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(
      model_name="gemini-2.0-flash-exp",
      generation_config=generation_config,
    )

    chat_session = model.start_chat(
      history=[
      ]
    )

    prompt = f"""create a sample resume for a junior software engineer and make the resume in markdown format and for th
              e ""jobs in:{data}"""  # prompt to generate the LLM for the generated resume
    response = chat_session.send_message(prompt)  # generates the resume

    print("Resume has been generated transferring resume to a text File now")
    generated_resume = response.text

    with open('resume.txt', 'w') as file:  # creates the txt file and writes the resume to the txt file.
        file.write(generated_resume)

    print("Resume has been transferred to the text file under resume.txt")


if __name__ == "__main__":
    main()
