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

role = "user"
prompt = "Explain how internet works?"

message = {
    "role" : role,
    "content" : prompt
}

messages = [message]


# Without stream
#response = client.chat.completions.create(model = model, messages = messages)
#print(response)
#answer = response.choices[0].message.content
#print(answer)


# With stream
response2 = client.chat.completions.create(model = model, messages = messages, stream = True)

for chunk in response2:
    content = chunk.choices[0].delta.content
    if content:
        print(content, end="", flush=True)
# here we use if content: bcz, agar content mai kuch ho, tb he print kro
# flush means turant aana chaiye
# We can use sleep() to make it more slow.