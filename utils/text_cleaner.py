import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from utils.nltk_setup import ensure_nltk_resources

# nltk.download("punkt")
# nltk.download("stopwords")

ensure_nltk_resources()



STOPWORDS = set(stopwords.words("english"))


def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(text)
    return [word for word in tokens if word.isalpha() and word not in STOPWORDS]
