"""
Contain the flow to convert the user prompt to effective search query.
"""

from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import word_tokenize


def prompt2query(prompt: str) -> str:
    tokens = word_tokenize(prompt)

    stop_words = set(stopwords.words("english"))
    tokens = [word for word in tokens if not word.lower() in stop_words]

    lemmatizer = SnowballStemmer('english')
    tokens = [lemmatizer.stem(word) for word in tokens]

    return ' '.join(tokens)


if __name__ == "__main__":
    user_input = "Tell me about elden ring"
    processed_query = prompt2query(user_input)
    print("Processed Query:", processed_query)
