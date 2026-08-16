import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer
import sys

model = SentenceTransformer("all-MiniLM-L6-v2")

load_dotenv()

my_api_key = os.getenv("GROQ_API_KEY").strip()

if not my_api_key:
    raise ValueError("api_Error")

client = Groq(api_key = my_api_key)
groqModel = "llama-3.3-70b-versatile"


documents = [
"Employees receive 24 days of paid leave per year.",

"Employees work from the office on Tuesday, Wednesday and Thursday. "
"Monday and Friday are optional work-from-home days.",

"Employees receive Rs 3000 per month for gym reimbursement.",

"Employees can claim Rs 2000 per month for home internet.",

"Employees have a 90 day notice period."
]


documents_embedding = model.encode(documents)
print(sys.getsizeof(documents_embedding))
# print(documents_embedding.nbytes)


# here, these 6 lines uses 780 bytes = 7kb
# if we have 6 lakh lines ---->  
# 7 kb * 1 lakh
# 7* 10^3 * 10^5
# 7 * 10^8
# 70 mb
# 
# It takes too much space , due to this we use Vector DB 

def cosine_similarity(a, b):
    return np.dot(a, b) / (
        np.linalg.norm(a) * np.linalg.norm(b)
    )





query = 'how much vacation do I get?'
query_embedding = model.encode(query)

def retrieve(query_embedding):
    scores = []

    for i , document in enumerate(documents_embedding):
        score = cosine_similarity(query_embedding, document)
        scores.append((score, documents[i]))
    scores.sort(reverse=True)
    return scores[0]



def ask_llm(question, context):
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
    response = client.chat.completions.create(model = groqModel, messages = messages)
    answer = response.choices[0].message.content
    return answer





query = 'how much vacation do I get?'
query_embedding = model.encode(query)
score, context = retrieve(query_embedding)
answer = ask_llm(query, context)
print(answer)