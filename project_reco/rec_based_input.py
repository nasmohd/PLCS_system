import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load projects data
projects_df = pd.read_csv('projects.csv')

# Create TF-IDF vectorizer to compute similarities between projects and user interests
vectorizer = TfidfVectorizer()

# Compute TF-IDF matrix for project skills
project_skills_matrix = vectorizer.fit_transform(projects_df['project_skills'])

# Generate recommendations for each user
user_interests = [['data analysis', 'machine learning'], ['web development'], ['data visualization', 'graphic design']]
recommendations = []
for i, user_skills in enumerate(user_interests):
    user_email = f"user_{i}"
    user_interests_str = ", ".join(user_skills)
    
    # Compute user interests vector using the same TF-IDF vectorizer
    user_skills_vector = vectorizer.transform([user_interests_str])
    
    # Compute similarity between user interests and each project
    project_similarities = cosine_similarity(user_skills_vector, project_skills_matrix).flatten()

    # Get indices of projects that have at least one skill matching the user interests
    matching_projects_indices = [index for index, project in projects_df.iterrows() 
                                 if any(skill in user_skills for skill in project['project_skills'].split(', '))]
                                 
    # Sort matching projects by similarity and recommend top 10
    matching_project_similarities = project_similarities[matching_projects_indices]
    matching_projects_indices_sorted = matching_project_similarities.argsort()[::-1][:10]
    recommended_projects = list(projects_df.iloc[matching_projects_indices[matching_projects_indices_sorted]]['project_id'])
    recommendations.append({'email': user_email, 'interests': user_interests_str, 'recommended_projects': recommended_projects})

# Write recommendations to a new CSV file
recommendations_df = pd.DataFrame(recommendations)
recommendations_df.to_csv('recommendations.csv', index=False)
