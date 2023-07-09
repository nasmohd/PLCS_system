import textdistance

def is_answer_correct(user_answer, recorded_answer):
    similarity = textdistance.jaccard(user_answer, recorded_answer)
    similarity_threshold = 0.744

    if similarity >= similarity_threshold:
        return True
    else:
        return False

# Example usage
user_answer = "The capital city of France is Paris"
recorded_answer = "Paris serves as the capital of France."

correct = is_answer_correct(user_answer, recorded_answer)
print(correct)  # Output: True
