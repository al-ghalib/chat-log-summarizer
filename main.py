import os
from summarizer.summarizer import summarize_chat


def summarize_folder(folder_path="chat-logs", use_tfidf=False):
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            summarize_chat(os.path.join(folder_path, filename), use_tfidf)


if __name__ == "__main__":
    summarize_folder(use_tfidf=True)
