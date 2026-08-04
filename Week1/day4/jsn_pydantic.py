import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

my_api_key = os.getenv("GROQ_API_KEY").strip()

if not my_api_key:
    raise ValueError("api_Error")


client = Groq(api_key = my_api_key)

model = "llama-3.3-70b-versatile"

role = "user"



# structure it

from pydantic import BaseModel;
class Ticket(BaseModel):
    name:str
    email:str
    issue:str

schema = Ticket.model_json_schema();

response_format = {
    "type": "json_object"
}

system_prompt = f"""
Extract the personal information and configure the issue from the ticket strictly based on schema and give a json output.
{schema}
"""

message_system = {
    "role": "system",
    "content": system_prompt
}

text = "Hello My name is Paras , I bought iphone and it is not working, my email is abc@gmail.com and phone number is 99999"

prompt = f"""
This is a customer ticket. Please extract personal information from this.
{text}
"""

message ={
        "role" : role,
        "content" : prompt
    }

messages = [message_system, message]


response = client.chat.completions.create(model = model, messages = messages, response_format = response_format)

answer = response.choices[0].message.content


print(response.choices[0].message.content)


# ab koi aage es code ko kyse padega
import json
raw_json= answer
# now makes it data file. and converts JSON string into python dictionary.
data_file=json.loads(raw_json)
# ** unpack to python dictionary and ticket become an object.
ticket = Ticket(**data_file)

print(ticket.name)
print(ticket.email)
print(ticket.issue)