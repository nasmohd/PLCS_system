import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Load projects data
projects_df = pd.read_csv('projects.csv')

# Load users data
users_df = pd.read_csv('users.csv')

# Create TF-IDF vectorizer to compute similarities between projects and user interests
vectorizer_skills = TfidfVectorizer()

# Compute TF-IDF matrix for project skills
project_skills = projects_df['project_skills']
project_skills_vector = vectorizer_skills.fit_transform(project_skills)

# Perform K-means clustering on project skills
k = 10  # Number of clusters
kmeans_model = KMeans(n_clusters=k, random_state=42)
kmeans_model.fit(project_skills_vector)

# Generate recommendations for each user
recommendations = []
for _, user in users_df.iterrows():
    user_email = user['email']
    user_interests = user['interests']
    if isinstance(user_interests, str):
        user_skills = [interest.strip() for interest in user_interests.strip('[]').split(',')]
    else:
        user_skills = user_interests
    
    # Compute user interests vector using the same TF-IDF vectorizer
    user_skills_vector = vectorizer_skills.transform(user_skills)
    
    # Predict the cluster label for the user interests
    cluster_label = kmeans_model.predict(user_skills_vector)[0]
    
    # Get projects that belong to the same cluster as user interests
    projects_in_cluster = projects_df[kmeans_model.labels_ == cluster_label]['project_id'].tolist()
    
    # Sort projects by their relevance to the cluster and recommend top 10
    recommended_projects = sorted(projects_in_cluster, key=lambda x: cosine_similarity(user_skills_vector, vectorizer_skills.transform([projects_df.loc[projects_df['project_id'] == x, 'project_skills'].values[0]]))[0][0], reverse=True)[:10]
    recommendations.append({'email': user_email, 'interests': user_interests, 'recommended_projects': recommended_projects})

# Write recommendations to a new CSV file
recommendations_df = pd.DataFrame(recommendations)
recommendations_df.to_csv('recommendations.csv', index=False)
