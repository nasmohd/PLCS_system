import nltk
# nltk.download('stopwords')
# nltk.download('omw-1.4')
# nltk.download('all')
# nltk.download('punkt')
# nltk.download('wordnet')
# nltk.download('omw-1.4')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.metrics import edit_distance

def is_answer_correct(user_answer, recorded_answer):
    # Tokenize and preprocess the sentences
    user_tokens = preprocess_sentence(user_answer)
    recorded_tokens = preprocess_sentence(recorded_answer)

    # Calculate the similarity or distance between the tokens
    similarity = calculate_similarity(user_tokens, recorded_tokens)

    # Define a threshold for similarity
    similarity_threshold = 0.8

    # Compare the similarity to the threshold
    if similarity >= similarity_threshold:
        return True
    else:
        return False

def preprocess_sentence(sentence):
    # Tokenize the sentence into words
    tokens = word_tokenize(sentence)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word.lower() not in stop_words]

    # Lemmatize the words
    lemmatizer = WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(word) for word in tokens]

    return tokens

def calculate_similarity(tokens1, tokens2):
    # Calculate the edit distance between the tokens
    distance = edit_distance(tokens1, tokens2)

    # Normalize the distance by the length of the longest token sequence
    max_length = max(len(tokens1), len(tokens2))
    similarity = 1 - (distance / max_length)

    return similarity

# Example usage
user_answer = "mitochondria is the power house of the cell"
recorded_answer = "mitochondria provides power to the cell"

correct = is_answer_correct(user_answer, recorded_answer)
print(correct)  # Output: True
