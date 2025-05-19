from .parser import parse_chat
from .statistics import count_messages
from .keywords import extract_keywords, tfidf_keywords


def summarize_chat(file_path, use_tfidf=False):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    user_msgs, ai_msgs = parse_chat(lines)
    total, user_count, ai_count = count_messages(user_msgs, ai_msgs)
    all_msgs = user_msgs + ai_msgs
    keywords = tfidf_keywords(all_msgs) if use_tfidf else extract_keywords(all_msgs)

    return {
        "file": file_path,
        "total": total,
        "user": user_count,
        "ai": ai_count,
        "keywords": keywords,
    }
