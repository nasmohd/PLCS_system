import random
import string
import pandas as pd

# Generate random movie titles and descriptions
def generate_movies(num_movies):
    titles = []
    descriptions = []
    for i in range(num_movies):
        # Generate a random title of length 5-10
        title_length = random.randint(5, 10)
        title = ''.join(random.choice(string.ascii_letters) for i in range(title_length))
        titles.append(title)

        # Generate a random description of length 20-50
        desc_length = random.randint(20, 50)
        description = ''.join(random.choice(string.ascii_letters) for i in range(desc_length))
        descriptions.append(description)

    return titles, descriptions

# Create a dataset with 500 movies
titles, descriptions = generate_movies(500)
movies_df = pd.DataFrame({'title': titles, 'description': descriptions})

# Save the dataset to a CSV file
movies_df.to_csv('movies.csv', index=False)

