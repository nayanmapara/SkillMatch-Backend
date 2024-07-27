import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Initialize Google AI Model
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
)

def enhance_resume(resume_content, job_description):
    chat_session = model.start_chat(
        history=[
        ]
    )
    input_text = f"Enhance the following resume content based on this job description:\n\nResume Content:\n{resume_content}\n\nJob Description:\n{job_description} and make the response into a latex format."
    response = chat_session.send_message(input_text)

    print(response.text)

    return response.text
