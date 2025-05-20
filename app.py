import os
import streamlit as st
from dotenv import load_dotenv
from chatlog_generator import generate_conversation, PROMPT_BANK, get_next_chat_number
from summarizer.summarizer import summarize_chat

load_dotenv()

# -----------------------------------Streamlit UI-----------------------------------
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


# Mode Selection
if "mode" not in st.session_state:
    st.session_state.mode = "Analyze Existing File"

mode = st.sidebar.radio(
    "Choose Mode:", ["Generate New Chat Logs", "Analyze Existing File"], index=1
)

text = ""

if mode == "Generate New Chat Logs":
    generate_count = st.sidebar.number_input(
        "Generate N chat logs", min_value=1, max_value=20, step=1
    )
    generate_btn = st.sidebar.button("⚙️ Generate Chats")

    # if generate_btn:
    #     with st.spinner(f"Generating {generate_count} short chats..."):
    #         last_file = ""
    #         for i in range(1, generate_count + 1):
    #             prompt = PROMPT_BANK[(i - 1) % len(PROMPT_BANK)]
    #             last_file = generate_conversation(prompt=prompt, turns=2, chat_num=i)
    #         with open(last_file, "r", encoding="utf-8") as f:
    #             text = f.read()
    #         st.success(
    #             f"✅ {generate_count} chats generated. Showing: `{os.path.basename(last_file)}`"
    #         )

    if generate_btn:
        with st.spinner(f"Generating {generate_count} short chats..."):
            start_index = get_next_chat_number()
            last_file = ""
            for i in range(start_index, start_index + generate_count):
                prompt = PROMPT_BANK[(i - start_index) % len(PROMPT_BANK)]
                last_file = generate_conversation(prompt=prompt, chat_num=i)
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

# Summary Output
if text:
    st.subheader("📄 Chat Log")
    st.code(text, language="text")

    analyze_btn = st.button("🔍 Analyze Chat")

    if analyze_btn:
        with st.spinner("Analyzing conversation..."):
            if mode == "Generate New Chat Logs":
                tmp_file = "chat_logs/_temp_summary.txt"
                with open(tmp_file, "w", encoding="utf-8") as f:
                    f.write(text)
                file_to_analyze = tmp_file
            else:
                file_to_analyze = os.path.join("chat_logs", selected_file)

            summary_data = summarize_chat(file_to_analyze, use_tfidf)

            st.subheader("📊 Summary")
            st.markdown(
                f"""
                - File: `{os.path.basename(summary_data['file'])}`  
                - The conversation had **{summary_data['total']} exchanges**  
                - User messages: **{summary_data['user']}**, AI messages: **{summary_data['ai']}**  
                - *{summary_data['topic']}* 
                - Most Common keywords: {', '.join(summary_data['keywords'][:5])}  
                """
            )
