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

def run_query(up):
    user_prompt = up
    
    model = SentenceTransformer("all-MiniLM-L6-v2")

    with open("../CorpusData/natmed_documents.json", "r", encoding="utf-8") as f:
        documents = json.load(f)
    
    index = faiss.read_index("../CorpusData/natmed_data.faiss")

    q_emb = model.encode([user_prompt], convert_to_numpy=True)
    D, I = index.search(q_emb, 3)
    results = [documents[i] for i in I[0]]
    context = ""
    for result in results:
        context += "Source: NatMedPro" + "-" + result["id"] + ": " + result["text"] + "                     "
        print(result["id"], ": ", result["text"])
    
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
    

if __name__ == "__main__":
    run_query("I've been thinking about trying L-Theanine. What are some positive effects that I can expect?")