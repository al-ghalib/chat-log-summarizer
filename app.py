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



##-------------------------Streamlit UI----------------------------##

st.title("🤖 AI Chat Log Summarizer")
st.sidebar.header("Options")
use_tfidf = st.sidebar.checkbox("Use TF-IDF", value=False)

if st.sidebar.button("🗑 Delete All Chat Logs"):
    deleted_files = 0
    for file in os.listdir("chat_logs"):
        if file.endswith(".txt"):
            os.remove(os.path.join("chat_logs", file))
            deleted_files += 1
    st.sidebar.success(f"Deleted {deleted_files} chat log(s)")

mode = st.sidebar.radio(
    "Choose Mode:", ["Generate New Chat Logs", "Analyze Existing File"]
)

text = ""


# Mode Selection

if mode == "Generate New Chat Logs":
    generate_count = st.sidebar.number_input(
        "Generate N chat logs", min_value=1, max_value=20, step=1
    )
    generate_btn = st.sidebar.button("⚙️ Generate Chats")

    if generate_btn:
        with st.spinner(f"Generating {generate_count} short chats..."):
            last_file = ""
            for i in range(1, generate_count + 1):
                prompt = PROMPT_BANK[(i - 1) % len(PROMPT_BANK)]
                last_file = generate_conversation(prompt=prompt, turns=2, chat_num=i)
            with open(last_file, "r", encoding="utf-8") as f:
                text = f.read()
            st.success(
                f"✅ {generate_count} chats generated. Showing: `{os.path.basename(last_file)}`"
            )

elif mode == "Analyze Existing File":
    chat_files = sorted([f for f in os.listdir("chat_logs") if f.endswith(".txt")])
    if not chat_files:
        st.warning("No chat logs found. Please generate some chats first.")
    else:
        selected_file = st.sidebar.selectbox("Choose a file", chat_files)
        if selected_file:
            with open(
                os.path.join("chat_logs", selected_file), "r", encoding="utf-8"
            ) as f:
                text = f.read()
            st.success(f"Loaded file: `{selected_file}`")



# ---------- Summary Output ----------
if text:
    st.text_area("📄 Chat Log", value=text, height=300)

    analyze_btn = st.button("🔍 Analyze Chat")

    if analyze_btn:
        with st.spinner("Analyzing conversation..."):
            total, user_count, ai_count, keywords = summarize_text(text, use_tfidf)
            lines = text.strip().split("\n")
            topic_line = lines[0]
            if topic_line.lower().startswith("# topic:"):
                main_topic = topic_line.replace("# Topic:", "").strip()
            elif topic_line.lower().startswith("user:"):
                main_topic = topic_line.replace("User:", "").strip().split("?")[0]
            else:
                main_topic = "a topic"

            st.subheader("📊 Summary")
            st.markdown(
                f"""
                - The conversation had **{total} exchanges**.  
                - The user asked mainly about **{main_topic}**.  
                - Top 5 most frequent keywords: {', '.join(keywords[:5])}.  
                """
            )
