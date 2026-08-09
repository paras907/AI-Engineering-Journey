import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY").strip()

if not my_api_key:
    raise ValueError("api_Error")


client = Groq(api_key = my_api_key)

model = "llama-3.3-70b-versatile"


# Knowledge base
knowledge_base = {
    "age" : "The age of pratyush is 25 years.",
    "Net Worth" : "the net worth of pratyush is 2000"
}

def retrieve_info(question):
    question = question.lower()
    if "age" in question:
        return knowledge_base["age"]
    elif "net worth" in question:
        return knowledge_base["Net Worth"]
    else:
        return None


def ask_llm(question):
    context = retrieve_info(question)
    sys_prompt = f"answer in one line only. only based on this context: {context}"

    system_message = {
        "role" : "system",
        "content" : sys_prompt
    }
    message= {
        "role" : "user",
        "content" : question
    }
    messages = [system_message, message]
    response = client.chat.completions.create(model = model, messages = messages)
    answer = response.choices[0].message.content
    return answer

question  = "do you konw pratyush's age and net worth?"

print(ask_llm(question))