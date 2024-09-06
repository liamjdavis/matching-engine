import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Step 1: Load CSV data into a DataFrame
csv_file_path = 'form_responses.csv'  # Replace with the path to your CSV file
df = pd.read_csv(csv_file_path)

df.columns = ['date', 'email', 'name', 'classYear', 'major1', 'major2', 'major3', 'interest', 'haveIdea','idea','stage','role','goals','addInfo','haveTeam','teamRegistered','teamEmail']

# Step 2: Specify the columns you want to use for similarity calculation
columns_to_use = ['major1', 'major2', 'major3','idea','addInfo']  # Replace with your desired columns

# Step 3: Extract the specified columns and concatenate their values for each row
row_texts = df[columns_to_use].astype(str).agg(' '.join, axis=1)

# Step 4: Initialize the TF-IDF Vectorizer
vectorizer = TfidfVectorizer()

# Step 5: Fit and transform the selected column data
tfidf_matrix = vectorizer.fit_transform(row_texts)

# Step 6: Compute cosine similarity between all rows based on the selected columns
cosine_sim_matrix = cosine_similarity(tfidf_matrix)

# Step 7: Output cosine similarity matrix between all rows
# The matrix shows the similarity between every pair of rows
similarity_df = pd.DataFrame(cosine_sim_matrix)

# Display the cosine similarity matrix
print("Cosine Similarity Between Rows Using Selected Columns:")
print(similarity_df)