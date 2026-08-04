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
# 3 prompts
prompt1 = "Hi!"
prompt2 = "Explain time travel in detail under 100 words"
prompt3 = "Write a 200 words essay on Machine learning"

prompts = [prompt1, prompt2, prompt3]
for prompt in prompts:
    message = {
            "role" : role,
            "content" : prompt
        }
    messages = [message]

    response = client.chat.completions.create(model = model, messages = messages, max_tokens=200)
    usage = response.usage
    print(f"Prompt: {prompt}, your_tokens: {usage.prompt_tokens}, completion_tokens: {usage.completion_tokens}, total_tokens: {usage.prompt_tokens+usage.completion_tokens}, Finish Reason: {response.choices[0].finish_reason}")
# Finish Reason determines why code stop due to token limit or any thing else.

#message = {
#            "role" : role,
#            "content" : prompt
#        }
#messages = [message]

#response = client.chat.completions.create(model = model, messages = messages)
#print(response)

#rint('#######################################')

#print(response.choices[0].message.content)