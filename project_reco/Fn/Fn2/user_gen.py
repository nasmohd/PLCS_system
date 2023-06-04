import csv
import random

skills = ['UI/UX', 'Web Application Development', 'Software Engineering', 'Algorithm', 'Data Structures', 'C++ Programming']

users = []
num_users = 100

for _ in range(num_users):
    email = f'user{random.randint(1, 1000)}@example.com'
    num_skills = random.randint(1, len(skills))
    user_skills = random.sample(skills, num_skills)
    users.append((email, user_skills))

# Write to CSV file
with open('Users.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Email', 'Skills'])
    writer.writerows(users)
