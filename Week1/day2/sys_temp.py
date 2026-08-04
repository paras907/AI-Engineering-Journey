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

'''
# System role example

role = "user"
prompt = "I love you mam!"

message_system = {
    "role" : "system",
    "content" : "You are strict office colleague who is also my manager"
}
'''

# Temperature example

role = "user"
prompt = "suggest a name for my food company"

message_system = {
    "role" : "system",
    "content" : "You are a brand manager who suggests name for my food company, name should in one word"
}

message = {
        "role" : role,
        "content" : prompt
    }

message = {
        "role" : role,
        "content" : prompt
    }

messages = [message_system, message]

response = client.chat.completions.create(model = model, messages = messages, temperature=2)
print(response)

print('#######################################')

print(response.choices[0].message.content)