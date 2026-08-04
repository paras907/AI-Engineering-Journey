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
prompt = "today's weather"

messages = [
    {
        "role" : role,
        "content" : prompt
    }
]

response = client.chat.completions.create(model = model, messages = messages)
print(response)

print('#######################################')

print(response.choices[0].message.content)