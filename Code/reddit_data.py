import json
import os

OUTPUT_FILE = "../RedditData/reddit_supplements_data.json"

def load_existing():
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_entry(entry):
    data = load_existing()
    data.append(entry)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def read_multiline(prompt="Post Body (end with a single '.' on its own line):"):
    print(prompt)
    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        if line.strip() == ".":
            break
        lines.append(line)
    return "\n".join(lines)

def main():

    while True:
        title = input("Post Title: ").strip()
        if title.lower() == "exit":
            break

        body = read_multiline()

        entry = {
            "title": title,
            "body": body
        }

        save_entry(entry)
        print("Saved!\n")

if __name__ == "__main__":
    main()
