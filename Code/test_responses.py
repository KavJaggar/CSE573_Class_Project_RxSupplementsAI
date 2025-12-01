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
from neo4j import GraphDatabase

def get_relationships(tx, name):
                query = """
                MATCH (n {name: $name})-[r]-(m)
                RETURN n, r, m
                """
                return list(tx.run(query, name=name))

def generate(user_prompt, url, payload):
    with requests.post(url, json=payload, stream=True) as response:
        outputstr = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode("utf-8"))
                token = data.get("response", "")
                print(token, end="", flush=True)
                outputstr += token
        toret = {}
        toret[user_prompt] = outputstr
        return toret


def run_query():
    
    model = SentenceTransformer("all-MiniLM-L6-v2")

    with open("../Data/CorpusData/natmed_documents.json", "r", encoding="utf-8") as f:
        documents = json.load(f)
    
    index = faiss.read_index("../Data/CorpusData/natmed_data.faiss")

    todump = []

    with open("../Evaluation/kgtestqs.txt", "r", encoding="utf-8") as f:
        for line in f:
            user_prompt = line.strip()
            print(user_prompt)

            # # #VECTOR RETRIEVAL
            # q_emb = model.encode([user_prompt], convert_to_numpy=True)
            # D, I = index.search(q_emb, 3)
            # results = [documents[i] for i in I[0]]
            context = ""
            # for result in results:
            #     context += result["id"] + ": " + result["text"] + "                     "
            #     #print(result["id"])
            
            #BM25 RETRIEVAL.
            def tokenize(text):
                return re.findall(r"\w+", text.lower())
            
            with open("../Data/CorpusData/bm25_index.pkl", "rb") as f:
                data = pickle.load(f)

            passages = data["documents"]
            bm25 = data["bm25"]

            tokenized_query = tokenize(user_prompt)

            scores = bm25.get_scores(tokenized_query)
            top_indices = scores.argsort()[::-1][:2]

            for idx in top_indices:
                context += str(passages[idx]) + "                   "
                #print(passages[idx], scores[idx])
            

            # KG SECTION
            sysprompt = """
            You are an AI that will help me extract the word of focus in questions that a user is asking me. They are asking me a question related to a supplement or medication.
            I need you to give me the item of focus in their question. 
            For Example:
            - What are the possible negative effects of creatine? -> creatine
            - Is my vitamin a supplement causing my skin to be itchy? -> vitamin a
            - Why should I take Vitamin B12 supplements? -> vitamin b12

            ONLY return the item of focus. Your response must also be in LOWER CASE ONLY.

            User's Question:

            """

            url = "http://10.21.58.251:11434/api/generate"

            payload = {
                "model": "mistral",
                "prompt": sysprompt + user_prompt,
                "stream": True
            }

            focus = ""
            with requests.post(url, json=payload, stream=True) as response:
                for line in response.iter_lines():
                    
                    if line:
                        data = json.loads(line.decode("utf-8"))
                        token = data.get("response", "")
                        focus += token

            print(focus)

            relevant_kg_results = """
            Relevant Facts from the NatMedPro Knowledge Graph:

            """
            try:
                 
                uri = "bolt://localhost:7687"
                user = "neo4j"
                password = "CSE573PASS"

                driver = GraphDatabase.driver(uri, auth=(user, password))

                kg_results = ""

                with driver.session() as session:
                    result = session.execute_write(get_relationships, focus.strip().lower())

                    for record in result:
                        n = record["n"]
                        r = record["r"]
                        m = record["m"]

                        kg_results += f"{n['name']} {r.type} {m['name']}    "


                sysprompt = f"""
                You are an AI that will help me determine the relevant facts to the question a user is asking me. I will give you a list of facts and you will return to me the ones that are VERY DIRECTLY relevant
                to answering the user's question. You can ONLY return up to 3 of the most relevant facts. If the facts are not relevant to answering the question, then do not return them. Do not try to force 
                3 facts, it is ok to return less, or even none. DO NOT return facts that do not directly relate to answering the user's question. 

                YOU CAN ONLY RETURN UP TO 3 FACTS MAXIMUM. THIS IS A HARD LIMIT THAT CANNOT BE EXCEEDED. 3 FACTS AT MOST.

                Facts:
                {kg_results}

                User's Question:

                """

                url = "http://10.21.58.251:11434/api/generate"

                payload = {
                    "model": "mistral",
                    "prompt": sysprompt + user_prompt,
                    "stream": True
                }

                with requests.post(url, json=payload, stream=True) as response:
                    for line in response.iter_lines():
                        
                        if line:
                            data = json.loads(line.decode("utf-8"))
                            token = data.get("response", "")
                            relevant_kg_results += token
            except:
                 pass

            print("KG Res:", relevant_kg_results)


            ### END KG SECTION ###

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

            toins = generate(user_prompt, url, payload)
            todump.append(toins)
            print() #newline
            print() #newline

    with open("../Evaluation/kgtestqsresponsesBM25ONLY.json", "w", encoding="utf-8") as f:
        json.dump(todump, f, ensure_ascii=False, indent=4)



if __name__ == "__main__":
    run_query()