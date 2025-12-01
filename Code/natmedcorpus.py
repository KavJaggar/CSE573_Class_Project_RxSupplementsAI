import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

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
                documents.append({
                    "id": f"Source: NatMedPro-{herb}-{section_name}-{idx}",
                    "herb": herb,
                    "section": section_name,
                    "text": chunk
                })
    
with open(f"../RedditData/reddit_supplements_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
for content in data:
    chunks = chunk_text(content["body"], max_length=150) 
    for idx, chunk in enumerate(chunks):
        documents.append({
            "id": f"Source: Reddit-{content["title"]}-{idx}",
            "herb": "",
            "section": "",
            "text": chunk
        })
    
model = SentenceTransformer("all-MiniLM-L6-v2")
texts = [d["text"] for d in documents]
embeddings = model.encode(texts, convert_to_numpy=True)
d = embeddings.shape[1]  # 384 for MiniLM
index = faiss.IndexFlatL2(d)
index.add(embeddings)

faiss.write_index(index, "../CorpusData/natmed_data.faiss")
with open("../CorpusData/natmed_documents.json", "w", encoding="utf-8") as f:
    json.dump(documents, f, ensure_ascii=False, indent=4)


    

