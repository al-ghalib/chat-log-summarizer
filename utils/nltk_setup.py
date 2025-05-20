import nltk

def ensure_nltk_resources():
    for resource in ["punkt", "stopwords"]:
        try:
            if resource == "punkt":
                nltk.data.find("tokenizers/punkt")
            else:
                nltk.data.find(f"corpora/{resource}")
        except LookupError:
            nltk.download(resource)
