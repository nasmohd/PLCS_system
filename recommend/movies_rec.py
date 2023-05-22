import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer

# Load the movie dataset
movies_df = pd.read_csv('movies.csv')

# Create a CountVectorizer object to convert the movie titles into vectors
count_vectorizer = CountVectorizer(stop_words='english')
count_matrix = count_vectorizer.fit_transform(movies_df['title'])

# Compute the cosine similarity between the movie vectors
cosine_sim = cosine_similarity(count_matrix, count_matrix)

# Define a function to get the top N similar movies for a given movie title
def get_similar_movies(title, cosine_sim=cosine_sim, movies_df=movies_df, top=10):
    # Get the index of the movie title in the movies dataframe
    idx = movies_df[movies_df['title'] == title].index[0]

    # Get the cosine similarity scores for all movies
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Sort the movies by similarity score
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the top N similar movies
    sim_scores = sim_scores[1:top+1]
    movie_indices = [i[0] for i in sim_scores]

    return movies_df.iloc[movie_indices]['title']

# Example usage
get_similar_movies('The Dark Knight', top=5)


"""
    "vectors" refer to the numerical representations of the movie titles. 
    To use the movie titles as input to a machine learning model, we need to convert them into a numerical format that the model can process.
    One common way to do this is to represent each movie title as a vector of numbers.

    In this particular code, the vectors are created using the CountVectorizer 
    class from the scikit-learn library. This class converts a collection of text documents 
    (in this case, the movie titles) into a matrix of token counts. Each row of the matrix represents a document, 
    and each column represents a unique token (in this case, a unique word in the movie titles). 
    The values in the matrix indicate the frequency of each token in each document.
"""


"""
    we load a movie dataset, convert the movie titles into vectors using CountVectorizer, 
    and compute the cosine similarity between the vectors. Then, we define a function to get 
    the top N similar movies for a given movie title based on the cosine similarity scores. 
    Finally, we test the function by getting the top 5 similar movies for "The Dark Knight".
"""