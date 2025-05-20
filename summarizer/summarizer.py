import os
import openai
from dotenv import load_dotenv
from .parser import parse_chat
from .statistics import count_messages
from .keywords import extract_keywords, tfidf_keywords

load_dotenv()

openai.api_key = os.getenv("GROQ_API_KEY")
openai.api_base = "https://api.groq.com/openai/v1"


def generate_topic_summary(chat_text: str, model="llama3-70b-8192") -> str:
    prompt = f"""
Analyze the following conversation between a User and an AI, and describe what the discussion is about in one sentence. Focus on the general purpose or theme of the interaction.

Conversation:
{chat_text}

Return only one sentence that describes the nature of this conversation.
"""
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_tokens=60,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[Topic Error: {str(e)}]"


def summarize_chat(file_path, use_tfidf=False):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    chat_text = "".join(lines)
    user_msgs, ai_msgs = parse_chat(lines)
    total, user_count, ai_count = count_messages(user_msgs, ai_msgs)
    all_msgs = user_msgs + ai_msgs
    keywords = tfidf_keywords(all_msgs) if use_tfidf else extract_keywords(all_msgs)
    topic = generate_topic_summary(chat_text)

    return {
        "file": file_path,
        "total": total,
        "user": user_count,
        "ai": ai_count,
        "keywords": keywords,
        "topic": topic,
    }
