import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load the data
def rec():
    users_df = pd.read_csv("users.csv")
    projects_df = pd.read_csv("projects.csv")

    # Step 2: Preprocess the data
    user_interests = users_df['interests'].apply(eval).tolist()
    project_skills = projects_df['project_skills'].apply(eval).tolist()

    # Create a list of unique interests/skills
    all_interests = list(set([interest for interests in user_interests for interest in interests]))
    all_skills = list(set([skill for skills in project_skills for skill in skills]))

    # Create numerical vectors for users' interests and projects' skills
    user_vectors = np.zeros((len(user_interests), len(all_interests)))
    for i, interests in enumerate(user_interests):
        for interest in interests:
            user_vectors[i, all_interests.index(interest)] = 1

    project_vectors = np.zeros((len(project_skills), len(all_skills)))
    for i, skills in enumerate(project_skills):
        for skill in skills:
            project_vectors[i, all_skills.index(skill)] = 1

    # Step 3: Calculate cosine similarity
    similarity_matrix = cosine_similarity(user_vectors, project_vectors)

    # Step 4: Sort projects based on cosine similarity scores
    sorted_indices = np.argsort(similarity_matrix, axis=1)[:, ::-1]  # Descending order

    # Step 5: Write recommendations to a new CSV file for the first user
    num_recommendations = 10
    rec_df = pd.DataFrame(columns=['email', 'recommended_projects'])

    user_index = 0  # Index of the first user
    user = users_df['email'].iloc[user_index]
    user_recommendations = []

    for j in range(num_recommendations):
        project_index = sorted_indices[user_index, j]
        project_id = projects_df['project_id'].iloc[project_index]
        user_recommendations.append(project_id)

    # rec_df.loc[user_index] = [user, user_recommendations]

    # rec_df.to_csv('recOne_cosSim.csv', index=False)
    return user_recommendations


rec_proj = rec()
print (rec_proj)