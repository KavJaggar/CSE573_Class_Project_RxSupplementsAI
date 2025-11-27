import requests
import json

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
    user_prompt = "Explain quantum physics in simple terms. Be concise."
    stream_query(user_prompt)
