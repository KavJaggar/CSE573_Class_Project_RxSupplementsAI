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

def run_query():
    
    def tokenize(text):
        return re.findall(r"\w+", text.lower())

    output = []

    with open("../CorpusData/bm25_index.pkl", "rb") as f:
        data = pickle.load(f)
    
    passages = data["documents"]
    bm25 = data["bm25"]

    with open("../Evaluation/evaluationquestions.txt", "r", encoding="utf-8") as f:
        for line in f:
            user_prompt = line.strip()
            print(user_prompt)
            tokenized_query = tokenize(user_prompt)
            scores = bm25.get_scores(tokenized_query)
            top_indices = scores.argsort()[::-1][:3]
            toins = {}
            toins[user_prompt] = {}
            for idx in top_indices:
                toins[user_prompt][f"result{idx}"] = (passages[idx], scores[idx])
            
            output.append(toins)
            
    
    with open("../Evaluation/BM25RetrievalTest.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    

if __name__ == "__main__":
    run_query()