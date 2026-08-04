import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

import pypdf

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API Error")

my_api_key = my_api_key.strip()

client = Groq(api_key = my_api_key)

model = "llama-3.3-70b-versatile"



def read_pdf(file_name):
    # if file is not in pdf format.
    if not file_name.lower().endswith(".pdf"):
        print("Enter pdf file")
        return

    complete_text = ""
    try:
        # read pdf file.
        with open(file_name, "rb") as file:
            reader = pypdf.PdfReader(file)

            print("Successfully read")

            for page in reader.pages:
                text = page.extract_text()
                if text:
                    complete_text += text + "\n"

    except FileNotFoundError:
        print("Not found")
        return None

    return complete_text


user_input = input("Enter the resume in (.pdf) format.")
user_resume = read_pdf(user_input)


job_des = input("Enter the job description in (.pdf) format.")
complete_job_des = read_pdf(job_des)




def ask_llm(system_prompt, user_prompt):
    system_message = {
        "role" : "system",
        "content" : system_prompt

    }
    user_message = {
        "role" : "user",
        "content" : user_prompt
    }

    messages = [system_message, user_message]

    response = client.chat.completions.create(model = model, messages = messages)
    answer = response.choices[0].message.content
    return answer


def extract_job_des(complete_job_des):
    system_prompt = """
    You are a professional HR assistant. Your work is to extract the data from the job description.
    Do not add any other information in it and use only the information give
    """
    user_prompt = f"""
    Extract the data from given job description.
    {complete_job_des}
    """
    return ask_llm(system_prompt, user_prompt)


def extract_resume(user_resume):
    system_prompt = """
    You are a professional HR assistant. Your work is to extract the data from the candidate's resume.
    Do not add any other information in it and use only the information give
    """
    user_prompt = f"""
    Extract the data from given resume.
    {user_resume}
    """
    return ask_llm(system_prompt, user_prompt)


def match_both(jd, res):
    system_prompt = """
        You are a professional HR assistant. Your work is to caompare the job description with candidate's resume.
        And generate the score between 1 to 100 from it to ensures that the candidate is how much fit for the given role.
        """
    user_prompt = f"""
        your work is to generate the score on the basis of job description and the resume data given .
        job description : {jd}
        resume : {res}
        """
    return ask_llm(system_prompt, user_prompt)



resume_data = extract_resume(user_resume)
job_data = extract_job_des(complete_job_des)
score = match_both(job_data, resume_data)
print(score)