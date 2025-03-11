import gui
import private
import google.generativeai as genai
from markdown_pdf import MarkdownPdf, Section

def create_reumse(user_input:dict,):
    resume =''
    genai.configure(api_key=private.API_KEY)  # Import API key

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

    converted_input = str(user_input)
    converted_job = str(gui.job_listing)
    prompt = (f"create a resume in markdown format based on the info provided here:{converted_input,converted_job}"
              f"with no markings and suggestions within the resume so it is a clean resume")
    # prompt to generate the LLM for the generated resume
    response = chat_session.send_message(prompt)  # generates the resume
    resume = response.text
    with open("resume.md", "w", encoding='utf-8') as f:
        f.write(resume)

    with open("resume.md", "r", encoding='utf-8') as f:
        text = f.read()
        pdf = MarkdownPdf()
        pdf.add_section(Section(text=text))
        pdf.meta["title"] = "resume.pdf"
        pdf.save("resume.pdf",)


