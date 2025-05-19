import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"

MODEL = "llama3-70b-8192"


def generate_conversation(prompt, turns=4):
    messages = [{"role": "user", "content": prompt}]
    log = []

    for _ in range(turns):
        response = openai.ChatCompletion.create(
            model=MODEL, messages=messages, temperature=0.7
        )
        ai_reply = response["choices"][0]["message"]["content"].strip()
        log.append(f"User: {messages[-1]['content']}")
        log.append(f"AI: {ai_reply}")
        messages.append({"role": "assistant", "content": ai_reply})
        messages.append({"role": "user", "content": "Tell me more."})
    return "\n".join(log)


def generate_multiple_chats(
    n=3, prompt="Tell me about Python and AI.", output_dir="chat_logs"
):
    os.makedirs(output_dir, exist_ok=True)
    for i in range(1, n + 1):
        text = generate_conversation(prompt)
        with open(f"{output_dir}/chat{i}.txt", "w", encoding="utf-8") as f:
            f.write(text)
