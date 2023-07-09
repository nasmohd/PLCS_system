from sentence_transformers import SentenceTransformer, util

def is_answer_correct(user_answer, recorded_answer):
    model = SentenceTransformer('bert-base-nli-mean-tokens')
    user_embedding = model.encode([user_answer])[0]
    recorded_embedding = model.encode([recorded_answer])[0]

    similarity = util.cos_sim(user_embedding, recorded_embedding)
    similarity_threshold = 0.8

    if similarity >= similarity_threshold:
        return True
    else:
        return False

# Example usage
user_answer = "mitochondria is the power house of the cell"
recorded_answer = "mitochondria provides power to the cell"

correct = is_answer_correct(user_answer, recorded_answer)
print(correct)  # Output: True
