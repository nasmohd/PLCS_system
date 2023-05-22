import pandas as pd
import random
import spacy

# Load English language model for spaCy
nlp = spacy.load('en_core_web_sm')

# Define list of skills
skills = ['C++ Programming', 'Java Programming', 'Android Mobile App Programming', 'Web Development', 'Data Analysis', 'Machine Learning', 'UI/UX Design']

# Define function to generate random project title
def generate_project_title(skill):
    prefix = random.choice(['Develop', 'Build', 'Create', 'Design', 'Implement', 'Code'])
    suffix = random.choice(['Project', 'App', 'System', 'Tool', 'Platform'])
    return f"{prefix} a {skill} {suffix}"

# Define function to generate random project description
def generate_project_description(skill):
    months = random.randint(3, 6)
    team_size = random.randint(2, 6)
    return f"This project involves {skill} and requires a team of {team_size} developers proficient in {skill}. The project will involve {months} months of work and a budget of ${random.randint(30000, 400000)}."

# Generate data for 1000 projects
projects_data = []
for i in range(1000):
    skill = random.choice(skills)
    title = generate_project_title(skill)
    description = generate_project_description(skill)
    project_skills = [skill]
    if random.random() > 0.5:
        additional_skill = random.choice([s for s in skills if s != skill])
        project_skills.append(additional_skill)
    projects_data.append({'project_title': title, 'project_description': description, 'project_skills': project_skills})

# Create dataframe
projects_df = pd.DataFrame(projects_data)

# Generate random project budgets
project_budgets = [random.randint(30000, 400000) // 500 * 500 for _ in range(1000)]
projects_df['project_budget'] = project_budgets

# Generate project IDs
project_ids = ['PLCS' + str(i).zfill(4) for i in range(1, 1001)]
projects_df['project_id'] = project_ids

# Generate random project DORs (date of registration)
start_date = pd.to_datetime('2021-01-01')
end_date = pd.to_datetime('2022-12-31')
delta = end_date - start_date
project_dors = [start_date + pd.Timedelta(days=random.randint(0, delta.days)) for _ in range(1000)]
projects_df['project_DOR'] = project_dors

# Generate random project deadlines
project_deadlines = [start_date + pd.Timedelta(days=random.randint(30, 180)) for _ in range(1000)]
projects_df['project_deadline'] = project_deadlines

# Save data to csv file
projects_df.to_csv('projects.csv', index=False)
