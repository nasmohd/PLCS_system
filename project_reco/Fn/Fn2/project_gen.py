import csv
import random

skills = ['UI/UX', 'Web Application Development', 'Software Engineering', 'Algorithm', 'Data Structures', 'C++ Programming']

projects = []
num_projects = 100

for i in range(num_projects):
    project_id = f'project-{i+1}'
    num_skills = random.randint(1, len(skills))
    project_skills = random.sample(skills, num_skills)
    projects.append((project_id, project_skills))

# Write to CSV file
with open('Projects.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Project ID', 'Skills'])
    writer.writerows(projects)
