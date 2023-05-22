import pandas as pd
import random

# Define list of skills
skills = ['C++ programming', 'Java programming', 'Android mobile App programming', 'Web development', 'Data analysis', 'Machine learning', 'UI/UX design']

# Define function to generate random project title
def generate_project_title(skill):
    prefix = random.choice(['Develop', 'Build', 'Create', 'Design', 'Implement', 'Code'])
    suffix = random.choice(['project', 'app', 'system', 'tool', 'platform'])
    return f"{prefix} a {skill} {suffix}"

# Generate data for 150 projects
projects_data = []
for i in range(150):
    skill = random.choice(skills)
    title = generate_project_title(skill)
    description = f"This project involves {skill} and requires a team of developers proficient in {skill}. The project will involve {random.randint(3, 6)} months of work."
    projects_data.append({'title': title, 'description': description})

# Create dataframe
projects_df = pd.DataFrame(projects_data)

# Save data to csv file
projects_df.to_csv('projects.csv', index=False)
