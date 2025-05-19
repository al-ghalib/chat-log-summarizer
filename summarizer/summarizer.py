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

    summary = f"""
        Summary of {file_path}:
        - Total messages exchanged: {total}
        - User messages: {user_count}, AI messages: {ai_count}
        - Top keywords: {', '.join(keywords)}
    """
    print(summary)
