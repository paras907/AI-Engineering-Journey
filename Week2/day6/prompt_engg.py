import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("api_Error")

client = Groq(api_key = my_api_key)
model = "llama-3.3-70b-versatile"


def llm_ans(prompt):
    message = {
    "role" : "user",
    "content" : prompt
    }

    messages = [message]
    response = client.chat.completions.create(model = model, messages = messages)
    answer = response.choices[0].message.content
    return answer


bad_prompt = """
this is a user complaint:
my laptop is not working
classify this
"""

good_prompt = """
#ROLE
you are a support assistant at a mobile/laptop company
#TASK
you have to classify issue in a category
#CONSTRAINT
you have to classify the issue in one of the three categories namely billing, technical, return.
#OUTPUT FORMAT
you answer should be in one word only. The one word should be of the categories given in constraints.
#EXAMPLE
if some say my phone hangs , put it under technical
#FALLBACK
if some ask the issue not related to product then put it under other
this is a user complaint:
my gf broke with me
"""

print(llm_ans(good_prompt))