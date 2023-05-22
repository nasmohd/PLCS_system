import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load data
projects_df = pd.read_csv('projects.csv')

# Preprocess project descriptions
tfidf = TfidfVectorizer(stop_words='english')
projects_df['description'] = projects_df['description'].fillna('')
tfidf_matrix = tfidf.fit_transform(projects_df['description'])

# Compute similarity matrix
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

def get_project_recommendations(title, cosine_sim=cosine_sim, df=projects_df):
    # Get index of project with matching title
    idx = df[df['title'] == title].index[0]

    # Get list of similar projects sorted by similarity score
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]

    # Get indices of similar projects
    project_indices = [i[0] for i in sim_scores]

    # Return recommended projects
    return df.iloc[project_indices]['title']
