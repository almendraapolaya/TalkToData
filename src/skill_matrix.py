import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Connecting to the Database:
load_dotenv()
connection_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
engine = create_engine(connection_url)

query = """
SELECT 
    js1.skill_abr AS skill_a, 
    js2.skill_abr AS skill_b, 
    COUNT(*) AS pair_frequency
FROM job_skills js1
JOIN job_skills js2 ON js1.job_id = js2.job_id
WHERE js1.skill_abr < js2.skill_abr
GROUP BY js1.skill_abr, js2.skill_abr
ORDER BY pair_frequency DESC
LIMIT 20;
"""

print("Querying database for top skill clusters...")

with engine.connect() as conn:
    df = pd.read_sql(text(query), conn)

matrix_df = df.pivot(index='skill_a', columns='skill_b', values='pair_frequency').fillna(0)

plt.figure(figsize=(12, 10))
sns.heatmap(matrix_df, annot=True, fmt=".0f", cmap="YlGnBu", cbar_kws={'label': 'Pair Frequency'})

plt.title("LinkedIn Job Postings: Top 20 Skill Co-occurrence Matrix", fontsize=16, fontweight='bold', pad=20)
plt.xlabel("Skill B", fontsize=12, labelpad=10)
plt.ylabel("Skill A", fontsize=12, labelpad=10)
plt.tight_layout()

output_path = "src/skill_clusters.png"
plt.savefig(output_path, dpi=300)
print(f"Success! Visual heatmap saved perfectly to: {output_path}")