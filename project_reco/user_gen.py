# Generate fake names for users
import pandas as pd
import random
import spacy
import faker

fake = faker.Faker()
first_names = [fake.first_name() for _ in range(1000)]
last_names = [fake.last_name() for _ in range(1000)]

# Define list of skills
skills = ['C++ Programming', 'Java Programming', 'Android Mobile App Programming', 'Web Development', 'Data Analysis', 'Machine Learning', 'UI/UX Design']


# Generate random emails for users
emails = [f"{first.lower()}.{last.lower()}@example.com" for first, last in zip(first_names, last_names)]

# Generate random interests for users
interests = [random.sample(skills, k=random.randint(3, len(skills))) for _ in range(1000)]

# Create dataframe for users
users_data = {'first_name': first_names, 'last_name': last_names, 'email': emails, 'interests': interests}
users_df = pd.DataFrame(users_data)

# Save data to csv files
users_df.to_csv('users.csv', index=False)