import gui
import private
import google.generativeai as genai
from markdown_pdf import MarkdownPdf, Section


"""
this file contains the code that prompts the LLM for the cover letter and resume and generates the markdown file whichis
then converted into a pdf
"""


def create_reumse(user_input: dict):
    resume = ''
    genai.configure(api_key=private.LLM_API_KEY)  # Import API key

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
    prompt = (f"create a cover letter in markdown format based on the info provided here:"
              f"{converted_job, converted_input}\n with no markings or suggestions so it is a clean cover letter")
    response = chat_session.send_message(prompt)
    cover_letter = response.text
    with open("cover_letter.md", "w", encoding="utf-8") as f:
        f.write(cover_letter)

    with open("cover_letter.md", "r", encoding="utf-8") as f:
        cover_letter = f.read()
        pdf = MarkdownPdf()
        pdf.add_section(Section(text=cover_letter))
        pdf.meta["title"] = "cover_letter.pdf"
        pdf.save("cover_letter.pdf")
    prompt = None
    prompt = (f"create a resume in markdown format based on the info provided here:{converted_input, converted_job}"
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
        pdf.save("resume.pdf", )
