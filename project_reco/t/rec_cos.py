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
"""
Specifically, it creates a sparse matrix where each row represents a project, 
and each column represents a word in the corpus of all project skills. 
The matrix stores the TF-IDF value for each word in each project.

This matrix can then be used to compute similarity between projects based on 
the skills they require, or to compute similarity between user interests and 
project skills, as in the example code.
"""


# Generate recommendations for each user
recommendations = []
for _, user in users_df.iterrows():
    user_email = user['email']
    user_interests = user['interests']
    user_skills = user_interests.split(', ')
    # Compute user interests vector using the same TF-IDF vectorizer
    user_skills_vector = vectorizer.transform([user_interests])
    # Compute similarity between user interests and each project
    project_similarities = cosine_similarity(user_skills_vector, project_skills_matrix).flatten()
    # Sort projects by similarity and recommend top 10
    recommended_projects_indices = project_similarities.argsort()[::-1][:10]
    recommended_projects = list(projects_df.iloc[recommended_projects_indices]['project_id'])
    recommendations.append({'email': user_email, 'interests': user_interests, 'recommended_projects': recommended_projects})

# Write recommendations to a new CSV file
recommendations_df = pd.DataFrame(recommendations)
recommendations_df.to_csv('recommendations.csv', index=False)


"""
In this code, we first compute the project_skills_matrix using the TfidfVectorizer. 
Then, for each user, we compute their interests vector using the same vectorizer and 
compute the cosine similarity between this vector and each project's vector in project_skills_matrix. 
Finally, we recommend the top 10 projects based on the similarity scores.
"""


"""
COSINE SIMILARITY
The cosine_similarity function takes two matrix inputs and returns the cosine similarity between them. 
In this case, the first matrix input is a vector representing the user's interests, and the second 
matrix input is a matrix where each row represents a project's set of required skills (encoded as TF-IDF 
vectors).

The output of cosine_similarity is a matrix where each row represents the cosine similarity between the 
user's interests and a project's set of required skills. The flatten() method is used to convert this 
matrix into a 1D array so that we can sort the projects by their similarity to the user's interests.
"""