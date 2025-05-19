from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from utils.text_cleaner import clean_text


def extract_keywords(messages, top_n=5):
    words = []
    for msg in messages:
        words.extend(clean_text(msg))
    return [word for word, _ in Counter(words).most_common(top_n)]


def tfidf_keywords(messages, top_n=5):
    vectorizer = TfidfVectorizer(stop_words="english", tokenizer=clean_text)
    X = vectorizer.fit_transform(messages)
    scores = X.sum(axis=0).A1
    words = vectorizer.get_feature_names_out()
    return [word for _, word in sorted(zip(scores, words), reverse=True)[:top_n]]
