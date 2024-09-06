import csv
import random
from datetime import datetime, timedelta

# Define possible values for each field
first_names = ["John", "Jane", "Alex", "Emily", "Michael", "Sarah", "David", "Lisa", "James", "Emma", "Daniel", "Olivia", "William", "Sophia", "Christopher", "Ava", "Matthew", "Isabella", "Andrew", "Mia"]
last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]
class_years = range(2024, 2029)
majors = ["Computer Science", "Economics", "Biology", "Physics", "Mathematics", "History", "Political Science", "Engineering", "Chemistry", "Psychology", "Sociology", "English", "Art History", "Environmental Science", "Philosophy", "Anthropology", "Neuroscience", "Statistics", "Music", "Linguistics"]
interests = ["Arts", "Education", "Finance", "Healthcare", "Sustainability", "Social Impact", "Technology", "Sports", "Entertainment", "Food & Beverage", "Fashion", "Travel", "Real Estate", "Marketing", "E-commerce"]
goals = ["Learn about entrepreneurship and startups", "Build relationships", "Test my current idea", "Solve world problems", "Win i2i's support", "Develop leadership skills", "Gain practical experience", "Explore new industries", "Network with professionals", "Enhance my resume", "Learn about venture capital", "Improve public speaking skills", "Understand market research", "Learn about intellectual property", "Develop project management skills"]
idea_stages = ["Concept", "Seed stage", "Development", "Prototype"]
roles = ["Business Strategy", "Engineering", "Financial"]

def generate_random_student():
    timestamp = datetime.now() - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    email = f"{first_name[0].lower()}{last_name.lower()}{random.randint(24,28)}@amherst.edu"
    full_name = f"{first_name} {last_name}"
    class_year = random.choice(class_years)
    major = random.choice(majors)
    additional_major_1 = random.choice(majors) if random.random() < 0.5 else ""
    additional_major_2 = random.choice(majors) if random.random() < 0.3 else ""
    domains_of_interest = ", ".join(random.sample(interests, random.randint(1, 5)))
    has_idea = random.choice(["Yes", "Not yet"])
    idea = "A new " + random.choice(["app", "platform", "device", "service", "product"]) if has_idea == "Yes" else ""
    idea_stage = random.choice(idea_stages) if has_idea == "Yes" else ""
    role = random.choice(roles)
    goals_for_lab = ", ".join(random.sample(goals, random.randint(1, 4)))
    additional_info = ""
    has_team = "No – match me with a team"
    team_registered = ""
    email_for_form = ""

    return [
        timestamp.strftime("%m/%d/%Y %H:%M:%S"),
        email,
        full_name,
        class_year,
        major,
        additional_major_1,
        additional_major_2,
        domains_of_interest,
        has_idea,
        idea,
        idea_stage,
        role,
        goals_for_lab,
        additional_info,
        has_team,
        team_registered,
        email_for_form
    ]

# Generate random data and write to CSV
num_students = 500  # You can change this to generate more or fewer students

with open('form_responses.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    
    # Write the header row
    writer.writerow([
        "Timestamp", "Email Address", "Full Name", "Class Year", "Major",
        "Additional Major 1", "Additional Major 2", "Domains of Interest",
        "Do you have an idea big or small?", "What is your idea?",
        "What stage are you at?", "What role are you interested in taking on a team?",
        "What are your goals for the Lab?", "Provide any additional information about yourself.",
        "Do you already have a team?", "Has your team been registered?",
        "If your team has not registered enter your email below and we will send you the form."
    ])
    
    # Generate and write random student data
    for _ in range(num_students):
        writer.writerow(generate_random_student())

print(f"Random data for {num_students} students has been generated and written to 'form_responses.csv'")