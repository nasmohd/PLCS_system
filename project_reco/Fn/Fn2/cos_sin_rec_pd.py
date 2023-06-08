import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load data from Users.csv and Projects.csv

# Load user data
users_df = pd.read_csv('Users.csv')
users = list(zip(users_df['Email'], users_df['Skills']))

# Load project data
projects_df = pd.read_csv('Projects.csv')
projects = list(zip(projects_df['Project ID'], projects_df['Skills']))

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
recommendations = []

for user_index, user in enumerate(users):
    email = user[0]

    # Get cosine similarity scores for the user
    user_sim_scores = cosine_sim_matrix[user_index]

    # Sort projects based on similarity scores
    sorted_indices = user_sim_scores.argsort()[::-1]

    # Get top 15 recommended projects
    num_projects = min(15, len(projects))
    recommended_projects = [projects[i][0] for i in sorted_indices[:num_projects]]

    recommendations.append([email, recommended_projects])

# Create a DataFrame from recommendations
recommendations_df = pd.DataFrame(recommendations, columns=['Email', 'Recommended Projects'])

# Write recommendations DataFrame to Cosine_sim.csv
recommendations_df.to_csv('Cosine_sim_pd.csv', index=False)
print (all_skills)