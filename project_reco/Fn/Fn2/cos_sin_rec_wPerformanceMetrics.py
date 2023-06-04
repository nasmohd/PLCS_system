import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import precision_score, recall_score, f1_score
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load data from Users.csv and Projects.csv

# Load user data
users = []
with open('Users.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        email = row[0]
        skills = row[1]
        users.append((email, skills))

# Load project data
projects = []
with open('Projects.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        project_id = row[0]
        skills = row[1]
        projects.append((project_id, skills))

# Step 2: Preprocess data and compute cosine similarity matrix

# Preprocess skills for CountVectorizer
all_skills = [user[1] for user in users] + [project[1] for project in projects]

# Create CountVectorizer and fit-transform the skills
vectorizer = CountVectorizer()
skills_matrix = vectorizer.fit_transform(all_skills)

# Compute cosine similarity matrix
user_skills = skills_matrix[:len(users)]
project_skills = skills_matrix[len(users):]
cosine_sim_matrix = cosine_similarity(user_skills, project_skills)

# Step 3: Generate recommendations and write to Cosine_sim.csv

# Write recommendations to Cosine_sim.csv
with open('Cosine_sim.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Email', 'Recommended Projects'])

    for user_index, user in enumerate(users):
        email = user[0]

        # Get cosine similarity scores for the user
        user_sim_scores = cosine_sim_matrix[user_index]

        # Sort projects based on similarity scores
        sorted_indices = user_sim_scores.argsort()[::-1]

        # Get top 15 recommended projects
        num_projects = min(15, len(projects))
        recommended_projects = [projects[i][0] for i in sorted_indices[:num_projects]]

        writer.writerow([email, recommended_projects])

# Step 4: Calculate performance metrics

ground_truth = []  # Ground truth data for relevant projects

# Populate ground truth data with relevant projects for each user (based on your criteria)

recommended_projects = []  # Recommended projects for each user

# Populate recommended_projects with the recommended projects from Cosine_sim.csv

# Calculate performance metrics
precision = precision_score(ground_truth, recommended_projects, average='micro', zero_division=1)
recall = recall_score(ground_truth, recommended_projects, average='micro', zero_division=1)
f1 = f1_score(ground_truth, recommended_projects, average='micro', zero_division=1)

# Print the calculated performance metrics
print("Precision:", precision)
print("Recall:", recall)
print("F1 Score:", f1)
