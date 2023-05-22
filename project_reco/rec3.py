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
        if any(skill in user_skills for skill in project_skills):
            recommended_projects.append(project_row['project_id'])
        if len(recommended_projects) >= 10:
            break
    recommendations.append({'email': user_email, 'interests': user_interests, 'recommended_projects': recommended_projects})

# Write recommendations to a new CSV file
recommendations_df = pd.DataFrame(recommendations)
recommendations_df.to_csv('recommendations.csv', index=False)


"""
This code is a Python script that generates project recommendations for each user based on their interests. 
It does this by computing similarities between the project skills (contained in the 'project_skills' column of the 'projects.csv' file) 
and the user interests (contained in the 'interests' column of the 'users.csv' file) using the TF-IDF vectorizer and cosine similarity 
metric provided by the Scikit-learn library.

The code first loads the 'projects.csv' and 'users.csv' files using the pandas library. It then creates a TF-IDF vectorizer object to 
generate a matrix of project skills using the fit_transform method of the vectorizer object.

The code then generates recommendations for each user in the 'users.csv' file by iterating through each user's interests and comparing 
them to each project's skills. If there is at least one skill in common between the user interests and project skills, 
the project is added to the recommended projects list. The recommendations are stored in a list of dictionaries, with each dictionary 
containing the email, interests, and recommended projects for a single user.

Finally, the recommendations are written to a new CSV file named 'recommendations.csv' using the to_csv method of the pandas 
DataFrame object.

"""