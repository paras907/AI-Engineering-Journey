
#             part 1   import and environments

import os
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
import numpy as np
from sentence_transformers import SentenceTransformer
import json


from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue, MatchAny, PayloadSchemaType


load_dotenv()

QDRANT_URL = os.getenv("QDRANT_URL")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY").strip()


print("API KEY LOADED =", bool(QDRANT_API_KEY))


#             part 2       connect to qdrant



client = QdrantClient(
    url = QDRANT_URL,
    api_key = QDRANT_API_KEY
)

print("Connected to Qdrant Cloud!")

print("Testing connection...")

collections = client.get_collections()

print("SUCCESS!")
print(collections)


#              part 3       create qdrant collections


COLLECTION_NAME = "knowledge_filter"
EMBEDDING_SIZE = 384

# delete collections if it already exists
if client.collection_exists(COLLECTION_NAME):
    print(f"Deleting existing collection: {COLLECTION_NAME}")
    client.delete_collection(COLLECTION_NAME)



# Create collections
client.create_collection(
    collection_name = COLLECTION_NAME,
    vectors_config= VectorParams(
        size = EMBEDDING_SIZE,
        distance = Distance.COSINE,
    ),
)

print(f"Createdd collection: {COLLECTION_NAME}")
print(f"Vector size: {EMBEDDING_SIZE}")
print(f"Distance: COSINE")
client.create_payload_index(
    collection_name=COLLECTION_NAME,
    field_name="category",
    field_schema=PayloadSchemaType.KEYWORD,
)



#          part 4      load our knowledge


with open("knowledge.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

print(f"Loaded {len(documents)} documents")



#            part 5          create embedding



print("Loading embedding model...")

model = SentenceTransformer("all-MiniLM-L6-v2")  # 384 size vector

print("Embedding model ready!")
texts = [document["text"] for document in documents]


embeddings = model.encode(texts)

print(f"Generated {len(embeddings)} embeddings")
print(f"Embedding size: {len(embeddings[0])}")



#             part 6  create qdrant points


points = []

for i in range(len(documents)):

    point = PointStruct(
        id = i+1,

        vector=embeddings[i].tolist(),

        payload=documents[i]
    )

    points.append(point)




#         part 7      upload to qdrant


client.upsert(   # upload + insert
    collection_name=COLLECTION_NAME,
    points=points
)

print(f"Uploaded {len(points)} documents to qdrant")



#             part 8     search qdrant


def search(query, top_k=3):

    #convert the question into an embedding
    query_vector = model.encode(query).tolist()

    # search Qdrant for similar vectors
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True,
    ).points

    return results

def search_with_filter(query, query_filter=None, top_k=3):

    query_vector = model.encode(query).tolist()

    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector,
        limit=top_k,
        with_payload=True,
        query_filter=query_filter
    ).points

    return results

reimbursement_filter = Filter(
    must=[
        FieldCondition(
            key="category",
            match=MatchValue(value="reimbursement")
        )
        # we can write, multiple fieldConditions
    ]
)



#         part 9   test result


query = "How many vacation days do I get?"

results = search_with_filter(query, reimbursement_filter, top_k=3)

print("\nSearch results:")

for result in results:
    print(f"Score: {result.score:.3f}")
    print(result.payload["text"])
    print()




#              part 10     connect to groq



groq_client = Groq(
    api_key=GROQ_API_KEY
)



#            part 11    ask the llm



def ask_llm(question, context):

    prompt = f"""
    Answer the question using only the information provided below.

    Context: {context}

    Question: {question}

    If the answer is not present in the context, say:
    "I don't know based on the provided information."
    """

    response = groq_client.chat.completions.create(
        model = "openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content



#            part 12     complete rag pipeline


question = "How many vacation days do I get?"

results = search_with_filter(question, reimbursement_filter, top_k=3)


# Extract text from the search results
context = "\n".join(
    result.payload["text"]
    for result in results
)



answer = ask_llm(question, context)

print("\nFinal Answer:")
print(answer)