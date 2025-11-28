from rank_bm25 import BM25Okapi
import re
import json
import pickle

def chunk_text(text, max_length):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_length):
        chunks.append(" ".join(words[i:i+max_length]))
    return chunks

documents = []

for i in range(2, 28):
    with open(f"../NatMedData/natmed_data{i}.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for herb, content in data.items():
        sections = content.get("sections", {})
        for section_name, section_text in sections.items():
            section_text = section_text.strip()
            chunks = chunk_text(section_text, max_length=150) 
            for idx, chunk in enumerate(chunks):
                documents.append(chunk)

passages = documents

def tokenize(text):
    return re.findall(r"\w+", text.lower())

tokenized_corpus = [tokenize(p) for p in passages]

bm25 = BM25Okapi(tokenized_corpus)

data = {
    "documents": passages,
    "bm25": bm25
}

with open("../CorpusData/bm25_index.pkl", "wb") as f:
    pickle.dump(data, f)
