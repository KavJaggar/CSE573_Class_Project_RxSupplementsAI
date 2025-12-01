from flask import Flask, request, jsonify
import requests
import query_phi

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate"

@app.route("/query", methods=["POST"])
def query_model():
    data = request.json
    prompt = data.get("prompt", "")

    payload = {
        "model": "phi3",
        "prompt": prompt,
        "stream": True
    }

    response = requests.post(OLLAMA_URL, json=payload)
    result = response.json()

    return jsonify({
        "response": result.get("response", "")
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
