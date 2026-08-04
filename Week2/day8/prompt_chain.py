import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from time import sleep

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

my_api_key = os.getenv("GROQ_API_KEY").strip()

if not my_api_key:
    raise ValueError("api_Error")


client = Groq(api_key = my_api_key)
model = "llama-3.3-70b-versatile"


JD = """
We are hiring a Backend python developer.

Requirements:
- Strong python
- FastAPI or Django
- PostgreSQL
- Docker
- AWS
-REST APIs
- 2+ years of experience
"""


RESUME = """
Name: Rahul Sharma

Experience:
Python, FastAPI, MySQL, Docker, REST APIs, GIT

Projects:
Built a food delivery backend using FastAPI and MySQL.

Deployed applications using Docker.
"""


def ask_llm(system_prompt, user_prompt):
    sys_msg = {
        "role" : "system",
        "content" : system_prompt
    }
    user_msg = {
        "role" : "user",
        "content" : user_prompt
    }
    messages = [sys_msg, user_msg]

    response = client.chat.completions.create(model = model, messages = messages)
    answer = response.choices[0].message.content
    return answer


def step1_res_extract(RESUME):
    system_prompt = """
    You are a professional HR assistant. Extract the skills from the candidates resume provided.
    Only return the skills , no other information. Do not invent any skills by yourself.
    output format:
    skills should be separated by commas. Just return comma separated skills don not return any filler information.
    """
    user_prompt = f"""
    Extract the skills from this resume
    {RESUME}
    """
    return ask_llm(system_prompt, user_prompt)


def step2_jd_extract(RESUME):
    system_prompt = """
    You are a professional HR assistant. Extract the skills from the job description provided.
    Only return the skills , no other information. Do not invent any skills by yourself.
    output format:
    skills should be separated by commas. Just return comma separated skills don not return any filler information.
    """
    user_prompt = f"""
    Extract the skills from this job description
    {JD}
    """
    return ask_llm(system_prompt, user_prompt)


def step3_match(candidate, jd):
    system_prompt = """
    You are a professional HR assistant. Compare the skills of candidate and the skills required in the JD and produce a final score between 1 and 100. Also produce a short verdice whether the candidate is a good fit for the role.
    """
    user_prompt = f"""
    Compare and match the skills
    JD: {jd}
    Candidate: {candidate}
    """
    return ask_llm(system_prompt, user_prompt)



candidate = step1_res_extract(RESUME)
sleep(2)
jd = step2_jd_extract(JD)
sleep(2)
score = step3_match(candidate, jd)
print(score)