import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load projects data
projects_df = pd.read_csv('projects.csv')

# Load users data
users_df = pd.read_csv('users.csv')

# Create TF-IDF vectorizer to compute similarities between projects and user interests
vectorizer = TfidfVectorizer()

# Compute TF-IDF matrix for project skills
project_skills_matrix = vectorizer.fit_transform(projects_df['project_skills'])

# Generate recommendations for each user
recommendations = []
for _, user in users_df.iterrows():
    user_email = user['email']
    user_interests = user['interests']
    user_skills = user_interests.split(', ')
    recommended_projects = []
    for project_index, project_row in projects_df.iterrows():
        project_skills = project_row['project_skills'].split(', ')
        if any(skill in project_skills for skill in user_skills):
            recommended_projects.append(project_row['project_id'])
        if len(recommended_projects) >= 10:
            break
    recommendations.append({'email': user_email, 'interests': user_interests, 'recommended_projects': recommended_projects})

# Write recommendations to a new CSV file
recommendations_df = pd.DataFrame(recommendations)
recommendations_df.to_csv('recommendations.csv', index=False)
