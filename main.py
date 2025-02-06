import private
import google.generativeai as genai  # CODE BELOW FOR THE MOST PART WAS TAKEN FROM PROVIDED CODE FROM GOOGLE AI


def main():


    genai.configure(api_key=private.API_KEY)
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

    with open('rapid_jobs2.json') as json_data:
        data = json_data.read()
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
