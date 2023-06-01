import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from your_app.models import User, Project

# Step 1: Load the data from Django models
users = User.objects.all()
projects = Project.objects.all()

# Create lists to store user interests and project skills
user_interests = [user.interests for user in users]
project_skills = [project.project_skills for project in projects]

# Step 2: Preprocess the data
# Rest of the code remains the same as the previous version
# ...

# Rest of the code remains the same as the previous version
# ...

# Step 5: Write recommendations to a new CSV file
num_recommendations = 10
rec_df = pd.DataFrame(columns=['email', 'recommended_projects'])

for i, user in enumerate(users):
    user_recommendations = []
    for j in range(num_recommendations):
        project_index = sorted_indices[i, j]
        project_id = projects[project_index].project_id
        user_recommendations.append(project_id)
    
    rec_df.loc[i] = [user.email, user_recommendations]

rec_df.to_csv('rec_cosSim.csv', index=False)
