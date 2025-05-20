import os
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk_data_dir = os.path.join(os.getcwd(), "nltk_data")
os.makedirs(nltk_data_dir, exist_ok=True)

nltk.download("punkt", download_dir=nltk_data_dir)
nltk.download("stopwords", download_dir=nltk_data_dir)

nltk.data.path.append(nltk_data_dir)

STOPWORDS = set(stopwords.words("english"))


def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(text)
    return [word for word in tokens if word.isalpha() and word not in STOPWORDS]
