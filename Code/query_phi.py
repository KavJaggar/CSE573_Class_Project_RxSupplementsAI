import requests
import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import re
import pickle
from rank_bm25 import BM25Okapi
from flask import Flask, request, Response, stream_with_context
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/run_query", methods=["POST"])
def run_query():
    data = request.get_json()
    user_prompt = data["prompt"]
    
    model = SentenceTransformer("all-MiniLM-L6-v2")

    with open("../Data/CorpusData/natmed_documents.json", "r", encoding="utf-8") as f:
        documents = json.load(f)
    
    index = faiss.read_index("../Data/CorpusData/natmed_data.faiss")

    q_emb = model.encode([user_prompt], convert_to_numpy=True)
    D, I = index.search(q_emb, 3)
    results = [documents[i] for i in I[0]]
    context = ""
    for result in results:
        context += result["id"] + ": " + result["text"] + "                     "
    
    #BM25 RETRIEVAL. DOES NOT WORK VERY WELL. JUST RETURNS NONSENSE IN TESTING SO FAR. BUT MODEL PERFORMS WELL WITH NOT BEING CONFUSED BY NONSENSICAL CONTEXT.
    # def tokenize(text):
    #     return re.findall(r"\w+", text.lower())
    
    # with open("../CorpusData/bm25_index.pkl", "rb") as f:
    #     data = pickle.load(f)

    # passages = data["documents"]
    # bm25 = data["bm25"]

    # tokenized_query = tokenize(user_prompt)

    # scores = bm25.get_scores(tokenized_query)
    # top_indices = scores.argsort()[::-1][:2]

    # for idx in top_indices:
    #     context += str(passages[idx]) + "                   "
    #     print(passages[idx], scores[idx])
    
    context = re.sub(r'\([\d,\s]+\)', '', context)


    prompt = f"""
                    You are a helpful medical assistant. 
                    ONLY use the information provided below only to answer the user's question. 
                    Do not mention the information, the source, or that you were given context. 
                    Do not say “according to the context,” “the document says,” or anything similar.

                    If the information is relevant, incorporate it naturally into your human-like answer. 
                    If it is not relevant, tell the user you do not know. 

                    Information:
                    "{context}"

                    User question:
                    {user_prompt}

                    Write a direct answer to the user and do not provide any information not necessary to answer their question. If some information does not relate to the user question, just ignore it.
                    Include citations to the sources of the information you use at the end of your answer. You can ONLY cite the sources found in the given context. ONLY the name of the source as provided.
                    DO NOT use any sources of information that are not explicitly provided to you.
                    """
    
    #print(prompt)
    url = "http://10.21.58.251:11434/api/generate"

    payload = {
        "model": "mistral",
        "prompt": prompt,
        "stream": True
    }

    def generate():
        with requests.post(url, json=payload, stream=True) as response:
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode("utf-8"))
                    token = data.get("response", "")
                    yield token
        
    return Response(stream_with_context(generate()),
                    mimetype="text/plain")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8181, debug=True)