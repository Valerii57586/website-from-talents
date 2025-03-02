import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter
import string


nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('punkt')


def extract_tags(content, tags_count):
    tags = ""
    filtered_words = []
    content = content.lower()
    content = re.sub(r"[^\w\s]", "", content)
    content = content.translate(str.maketrans('', '', string.punctuation))
    words = word_tokenize(content)
    stop_words = set(stopwords.words('russian'))
    for word in words:
        if word not in stop_words:
            filtered_words.append(word)
    word_counts = Counter(filtered_words)
    tags = word_counts.most_common(tags_count)
    return tags

