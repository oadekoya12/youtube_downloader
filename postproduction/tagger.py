# postproduction/tagger.py
import argparse
import json
import re

TAG_RULES = {
    "church": ["sermon", "worship", "praise", "forum", "scripture"],
    "podcast": ["host", "guest", "interview", "intro", "recap"],
    "business": ["presentation", "meeting", "keynote", "strategy", "q&a"],
    "generic": []
}

def load_text(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read().lower()

def tag_content(text, mode):
    rules = TAG_RULES.get(mode, [])
    return {tag: bool(re.search(rf"\b{tag}\b", text)) for tag in rules}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--transcript", required=True, help="Path to transcript")
    parser.add_argument("--mode", choices=TAG_RULES.keys(), default="generic")
    args = parser.parse_args()

    text = load_text(args.transcript)
    tags = tag_content(text, args.mode)
    tag_file = args.transcript.replace(".txt", f".{args.mode}.tags.json")

    with open(tag_file, "w") as f:
        json.dump(tags, f, indent=2)

    print(f"[✓] Tags saved to {tag_file}")
