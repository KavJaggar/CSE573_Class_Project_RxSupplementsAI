import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np


documents = []

for i in range(2, 28):

    with open("../NatMedData/natmed_data" + str(i) + ".json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for herb, content in data.items():
        sections = content.get("sections", {})
        for section_name, section_text in sections.items():
            documents.append({
                "id": f"{herb}-{section_name}",
                "herb": herb,
                "section": section_name,
                "text": section_text.strip()
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


    

