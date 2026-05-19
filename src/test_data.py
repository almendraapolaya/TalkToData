import pandas as pd


path = "/Users/emmyalmendra/Desktop/Code/LinkedIn Job Postings (2023 - 2024)/mappings/skills.csv"

df = pd.read_csv(path)
print("Success! Here are the first few rows of the skills dataset:")
print(df.head())