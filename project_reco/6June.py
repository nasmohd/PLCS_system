import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load user and project data
users_df = pd.read_csv('users.csv')
projects_df = pd.read_csv('projects.csv')

# Create TF-IDF vectors for user interests
tfidf_vectorizer = TfidfVectorizer()
user_interests_vectors = tfidf_vectorizer.fit_transform(users_df['interests'].apply(' '.join))

# Create TF-IDF vectors for project skills
project_skills_vectors = tfidf_vectorizer.transform(projects_df['project_skills'].apply(' '.join))

# Compute cosine similarity between user interests and project skills
cosine_sim = cosine_similarity(user_interests_vectors, project_skills_vectors)

# Initialize dictionary to store recommended projects for each user
recommendations = {'email': [], 'interests': [], 'recommended_projects': []}

# Recommend projects to each user
for user_index, user_row in users_df.iterrows():
    email = user_row['email']
    interests = user_row['interests']
    
    # Get cosine similarity scores for the current user
    user_scores = cosine_sim[user_index]
    
    # Sort projects based on similarity scores in descending order
    sorted_indices = user_scores.argsort()[::-1]
    
    # Select top 10 projects (or all projects if less than 10)
    top_projects = projects_df.loc[sorted_indices[:10], 'project_title']
    
    # Add user and recommended projects to the dictionary
    recommendations['email'].append(email)
    recommendations['interests'].append(interests)
    recommendations['recommended_projects'].append(list(top_projects))

# Create DataFrame from recommendations dictionary
recommendations_df = pd.DataFrame(recommendations)

# Save recommendations to a new CSV file
recommendations_df.to_csv('recommendations_6June.csv', index=False)
