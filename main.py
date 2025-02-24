import sql_functions
import private
import google.generativeai as genai


def upload_data1(
    data: list, cursor
):  # this functions adds data from rapid_jobs2 to the database
    x = 0
    sorted_data = {}
    import_data = {}
    conn, cursor = sql_functions.open_database("jobs_db.sqlite")
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


def upload_data2(
    data: list, cursor
):  # this function adds the data from rapidResults.json to database
    x = 0
    sorted_data = {}
    conn, cursor = sql_functions.open_database("jobs_db.sqlite")
    sql_functions.set_results_db(cursor)
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


def main():
    genai.configure(api_key=private.API_KEY)  # Import API key

    # Create the model and code for model creation was taken directly from google studio

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

    chat_session = model.start_chat(history=[])

    prompt = "create a sample resume for a junior software engineer and make the resume in markdown format and for the"
    # prompt to generate the LLM for the generated resume
    response = chat_session.send_message(prompt)  # generates the resume

    print("Resume has been generated transferring resume to a text File now")
    generated_resume = response.text

    with open(
        "resume.txt", "w"
    ) as file:  # creates the txt file and writes the resume to the txt file.
        file.write(generated_resume)

    print("Resume has been transferred to the text file under resume.txt")


if __name__ == "__main__":
    main()
