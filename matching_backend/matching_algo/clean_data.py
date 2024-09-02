import pandas as pd
import re
from sklearn.preprocessing import MultiLabelBinarizer

# Load CSV (all columns included)
df = pd.read_csv('form_responses.csv')

# Define the standard categories
domains_of_interest = ['arts', 'education', 'finance', 'healthcare', 'sustainability', 'social impact', 'technology']
goals_for_lab = ['learn about entrepreneurship and startups', 'build relationships', 'test my current idea', 'solve world problems', 'win i2i\'s support']
roles_interested = ['business strategy', 'engineering', 'financial']

# Cleaning function for text fields
def clean_text(text):
    if pd.isna(text):
        return ''
    text = text.strip().lower()  # Remove whitespace and convert to lowercase
    text = re.sub(r'\s*,\s*', ', ', text)  # Ensure consistent spacing
    return text

# Apply cleaning to the relevant columns
df['Domains of Interest'] = df['Domains of Interest'].apply(clean_text)
df['What are your goals for the Lab?'] = df['What are your goals for the Lab?'].apply(clean_text)
df['What role are you interested in taking on a team?'] = df['What role are you interested in taking on a team?'].apply(clean_text)

# Split and match against standard categories
df['Domains of Interest'] = df['Domains of Interest'].apply(lambda x: [domain for domain in domains_of_interest if domain in x])
df['What are your goals for the Lab?'] = df['What are your goals for the Lab?'].apply(lambda x: [goal for goal in goals_for_lab if goal in x])
df['What role are you interested in taking on a team?'] = df['What role are you interested in taking on a team?'].apply(lambda x: [role for role in roles_interested if role in x])

# Convert lists into binary encoded columns using MultiLabelBinarizer
mlb = MultiLabelBinarizer()

# Create binary features for Domains of Interest
df_domains = pd.DataFrame(mlb.fit_transform(df['Domains of Interest']), columns=mlb.classes_, index=df.index)

# Create binary features for Goals
df_goals = pd.DataFrame(mlb.fit_transform(df['What are your goals for the Lab?']), columns=mlb.classes_, index=df.index)

# Create binary features for Roles
df_roles = pd.DataFrame(mlb.fit_transform(df['What role are you interested in taking on a team?']), columns=mlb.classes_, index=df.index)

# Concatenate the original dataframe with the binary encoded features
df_profiles = pd.concat([df, df_domains, df_goals, df_roles], axis=1)

# Drop the original text columns that have been encoded
df_profiles.drop(['Domains of Interest', 'What are your goals for the Lab?', 'What role are you interested in taking on a team?'], axis=1, inplace=True)

# Filter to only include responses where "Do you already have a team?" is "No - match me with a team"
df_filtered = df_profiles[df_profiles['Do you already have a team?'] == 'No – match me with a team']

# Print the filtered and processed dataframe
pd.set_option('display.max_columns', None)
print(df_filtered.head())