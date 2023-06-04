#Use few projects

import csv
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load data from Users.csv and Projects.csv

# Load user data
users = []
with open('User_one.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the header row
    for row in reader:
        email = row[0]
        skills = row[1]
        users.append((email, skills))

# Load project data
projects = []
with open('Projects_10.csv', 'r') as csvfile:
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
# Step 4: Adjust similarity threshold and filter recommendations
# Write recommendations to Cosine_sim.csv
with open('Cosine_sim_few.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Email', 'Recommended Projects'])

    for user_index, user in enumerate(users):
        email = user[0]

        # Get cosine similarity scores for the user
        user_sim_scores = cosine_sim_matrix[user_index]

        # Sort projects based on similarity scores
        sorted_indices = user_sim_scores.argsort()[::-1]

        # Filter projects based on similarity threshold
        recommended_projects = []
        for index in sorted_indices:
            project_id = projects[index][0]
            project_skills = projects[index][1]
            user_skills = user[1]

            # Check if there is at least one matching skill
            matching_skills = set(project_skills.split()) & set(user_skills.split())
            if len(matching_skills) > 0:
                recommended_projects.append(project_id)
                if len(recommended_projects) == 15:
                    break

        writer.writerow([email, recommended_projects])
