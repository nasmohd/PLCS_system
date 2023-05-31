import pandas as pd
from surprise import Reader, Dataset, SVD
from surprise.model_selection import train_test_split

# Load projects data
projects_df = pd.read_csv('projects.csv')

# Load users data
users_df = pd.read_csv('users.csv')

# Prepare the data in the required format for Surprise library
reader = Reader(rating_scale=(0, 1))
data = Dataset.load_from_df(users_df[['email', 'interests', 'projects']], reader)

# Split the data into training and testing sets
trainset, testset = train_test_split(data, test_size=0.2, random_state=42)

# Train the collaborative filtering model (SVD)
model = SVD()
model.fit(trainset)

# Generate recommendations for each user
recommendations = []
for _, user in users_df.iterrows():
    user_email = user['email']
    user_interests = user['interests']
    user_skills = user_interests.split(', ')

    # Predict ratings for projects not rated by the user
    project_ratings = []
    for project_id in projects_df['project_id']:
        if project_id not in user['projects']:
            predicted_rating = model.predict(user_email, project_id).est
            project_ratings.append((project_id, predicted_rating))

    # Sort projects by predicted ratings and recommend top 10
    project_ratings.sort(key=lambda x: x[1], reverse=True)
    recommended_projects = [proj[0] for proj in project_ratings[:10]]
    recommendations.append({'email': user_email, 'interests': user_interests, 'recommended_projects': recommended_projects})

# Write recommendations to a new CSV file
recommendations_df = pd.DataFrame(recommendations)
recommendations_df.to_csv('recommendations.csv', index=False)
