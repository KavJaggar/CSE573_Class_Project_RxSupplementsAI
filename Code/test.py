import os
import json

def chunk_text(text, max_length):
    words = text.split()
    chunks = []
    for i in range(0, len(words), max_length):
        chunks.append(" ".join(words[i:i+max_length]))
    return chunks

documents = []

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

print(documents)
