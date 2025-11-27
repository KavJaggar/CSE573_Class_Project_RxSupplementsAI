import requests
import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re

def stream_query(prompt):
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": "phi3",
        "prompt": prompt,
        "stream": True
    }

    with requests.post(url, json=payload, stream=True) as response:
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                token = data.get("response", "")
                print(token, end="", flush=True)

    print()


if __name__ == "__main__":
    user_prompt = "I'm thinking about using creatine orally. Are there any potential side effects that I need to worry about?"
    
    model = SentenceTransformer("all-MiniLM-L6-v2")

    with open("../CorpusData/natmed_documents.json", "r", encoding="utf-8") as f:
        documents = json.load(f)
    
    index = faiss.read_index("../CorpusData/natmed_data.faiss")

    q_emb = model.encode([user_prompt], convert_to_numpy=True)
    D, I = index.search(q_emb, 1)
    results = [documents[i] for i in I[0]]
    context = ""
    for result in results:
        context += result["id"] + ": " + result["text"] + "\n"
    
    context = re.sub(r'\([\d,\s]+\)', '', context)


    prompt = f"""
            You are a helpful medical assistant. 
            ONLY use the information provided below only to answer the user's question. 
            Do not mention the information, the source, or that you were given context. 
            Do not say “according to the context,” “the document says,” or anything similar.

            If the information is relevant, incorporate it naturally into your answer. 
            If it is not relevant, tell the user you do not know. 

            Information:
            "{context}"
            Context Reference Source - NatMedPro

            User question:
            {user_prompt}

            Write a direct answer to the user. Include citations to the sources of the information you use at the end of your answer. Just mention the name of the sources like "Sources: ..."

            """
    
    print(prompt)
    stream_query(prompt)
