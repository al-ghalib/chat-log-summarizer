import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# nltk.download("punkt")
# nltk.download("stopwords")

try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")


STOPWORDS = set(stopwords.words("english"))


def clean_text(text):
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    tokens = word_tokenize(text)
    return [word for word in tokens if word.isalpha() and word not in STOPWORDS]
