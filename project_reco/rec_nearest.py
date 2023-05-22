import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors

# Load projects data
projects_df = pd.read_csv('projects.csv')

# Load users data
users_df = pd.read_csv('users.csv')

# Create TF-IDF vectorizer to compute similarities between projects and user interests
vectorizer = TfidfVectorizer()

# Compute TF-IDF matrix for project skills
project_skills_matrix = vectorizer.fit_transform(projects_df['project_skills'])

# Fit NearestNeighbors model to project skills matrix
nn_model = NearestNeighbors(n_neighbors=10)
nn_model.fit(project_skills_matrix)

# Generate recommendations for each user
recommendations = []
for _, user in users_df.iterrows():
    user_email = user['email']
    user_interests = user['interests']
    user_skills = user_interests.split(', ')
    # Compute user interests vector using the same TF-IDF vectorizer
    user_skills_vector = vectorizer.transform([user_interests])
    # Find nearest neighbors (i.e., recommended projects) to user interests vector
    _, recommended_projects_indices = nn_model.kneighbors(user_skills_vector)
    recommended_projects_indices = recommended_projects_indices.flatten()
    # Get recommended project IDs
    recommended_projects = list(projects_df.iloc[recommended_projects_indices]['project_id'])
    recommendations.append({'email': user_email, 'interests': user_interests, 'recommended_projects': recommended_projects})

# Write recommendations to a new CSV file
recommendations_df = pd.DataFrame(recommendations)
recommendations_df.to_csv('recommendations_nearest.csv', index=False)
