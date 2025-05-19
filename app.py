import os
import streamlit as st
from dotenv import load_dotenv
from chatlog_generator import generate_conversation, PROMPT_BANK
from summarizer.parser import parse_chat
from summarizer.statistics import count_messages
from summarizer.keywords import extract_keywords, tfidf_keywords

load_dotenv()

def summarize_text(text, use_tfidf=False):
    lines = text.strip().split("\n")
    user_msgs, ai_msgs = parse_chat(lines)
    total, user_count, ai_count = count_messages(user_msgs, ai_msgs)
    all_msgs = user_msgs + ai_msgs
    keywords = tfidf_keywords(all_msgs) if use_tfidf else extract_keywords(all_msgs)
    return total, user_count, ai_count, keywords


st.title("🤖 AI Chat Log Summarizer")

st.sidebar.header("Options")
use_tfidf = st.sidebar.checkbox("Use TF-IDF", value=False)
generate_count = st.sidebar.number_input(
    "Generate N chat logs", min_value=1, max_value=20, step=1
)
generate_btn = st.sidebar.button("Generate Chats")

text = ""

if generate_btn:
    with st.spinner(f"Generating {generate_count} short chats..."):
        last_file = ""
        for i in range(1, generate_count + 1):
            prompt = PROMPT_BANK[(i - 1) % len(PROMPT_BANK)]
            last_file = generate_conversation(prompt=prompt, turns=2, chat_num=i)
        with open(last_file, "r", encoding="utf-8") as f:
            text = f.read()
        st.success(
            f"✅ {generate_count} chats generated. Showing `{os.path.basename(last_file)}`"
        )

if text:
    st.text_area("📄 Chat Log", value=text, height=300)
    total, user_count, ai_count, keywords = summarize_text(text, use_tfidf)
    st.subheader("📊 Summary")
    st.write(f"**Total Messages:** {total}")
    st.write(f"**User Messages:** {user_count}")
    st.write(f"**AI Messages:** {ai_count}")
    st.write("**Top Keywords:**")
    st.markdown(", ".join(keywords))
