import os
import random
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

MODEL = "llama3-70b-8192"

PROMPT_BANK = [
    "How does AI impact daily life?",
    "What’s Python used for these days?",
    "Can you explain cloud computing like I’m five?",
    "Is NoSQL better than SQL?",
    "Tell me why ethics matter in AI.",
]

USER_REPLIES = [
    "Oh really?",
    "Can you explain a bit more?",
    "Interesting!",
    "What do you mean?",
    "Hmm, go on.",
]

SYSTEM_PROMPT = {
    "role": "system",
    "content": "You're having a casual conversation. Keep answers short (1-2 sentences), friendly, and verbal like texting.",
}


def generate_conversation(prompt, turns=None, chat_num=1, output_dir="chat_logs"):
    if turns is None:
        turns = random.randint(1, 4)

    messages = [SYSTEM_PROMPT, {"role": "user", "content": prompt}]
    log = []

    for _ in range(turns):
        try:
            response = openai.ChatCompletion.create(
                model=MODEL, messages=messages, temperature=0.8, max_tokens=60
            )
            ai_reply = response["choices"][0]["message"]["content"].strip()
            log.append(f"User: {messages[-1]['content']}")
            log.append(f"AI: {ai_reply}")
            user_follow_up = random.choice(USER_REPLIES)
            messages.append({"role": "assistant", "content": ai_reply})
            messages.append({"role": "user", "content": user_follow_up})
        except Exception as e:
            log.append(f"[Error]: {str(e)}")
            break

    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"chat{chat_num}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(log))
    return file_path


def get_next_chat_number(output_dir="chat_logs"):
    existing = [
        f for f in os.listdir(output_dir) if f.startswith("chat") and f.endswith(".txt")
    ]
    existing_nums = [int(f[4:-4]) for f in existing if f[4:-4].isdigit()]
    return max(existing_nums, default=0) + 1
