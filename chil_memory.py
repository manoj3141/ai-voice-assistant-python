import json
import os

MEMORY_FILE = "memory.json"
AI_MEMORY_FILE = "AiMemory.json"

def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r") as f:
        return json.load(f)


def save_memory(data):
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def remember(key, value):
    memory = load_memory()
    memory[key] = value
    save_memory(memory)

def recall(key):
    memory = load_memory()
    return memory.get(key, "")


#---------------AI Memory-----------

if os.path.exists(AI_MEMORY_FILE):
    with open(AI_MEMORY_FILE, "r", encoding="utf-8") as f:
        messages = json.load(f)
else:
    messages = [{
    "role": "system",
    "content": (
        # "You are a smart, funny, friendly assistant. "
        # "Talk naturally like a close friend. "
        # "Be warm, playful, helpful, concise, and non-robotic. "
        # "Support sad users and joke with funny users. "
        # "Never mention being an AI unless asked. "
        "Treat words like bro, dude, mamu, buddy, mate, nanba, homie, and pal as friendly nicknames referring to the user or a close friend."
        "Keep replies extremely short. "
        "Do not use emojis. "
        "Do not use bullet points, stars, dashes, hashtags, or special symbols. "
        "Reply only in plain simple text."
    )
}]

def save_AiMemory(messages):
    with open(AI_MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(messages, f, indent=2, ensure_ascii=False)