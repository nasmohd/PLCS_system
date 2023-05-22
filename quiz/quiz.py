import requests
from pyquiz import Question, Quiz

# Define the notes
notes = "The capital city of France is Paris. The Eiffel Tower is located in Paris. The Louvre Museum is also located in Paris."

# Set up API request
url = "https://quizgeneratorapi.com/api/v1/questions"
data = {"text": notes, "num_questions": 3}

# Send API request and retrieve questions as JSON data
response = requests.post(url, data=data)
questions = response.json()["data"]

# Create a quiz
quiz = Quiz("France Quiz")

# Add questions to quiz
for question in questions:
    question_text = question["question"]
    options = question["options"]
    correct_answer = options.index(question["answer"])
    q = Question(question_text, options, correct_answer)
    quiz.add_question(q)

# Print the quiz
print(quiz.to_json())
