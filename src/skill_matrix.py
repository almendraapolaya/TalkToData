import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

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
  AND (
      js1.skill_abr IN ('IT', 'ENG', 'MGMT', 'ANLS', 'PRJM', 'SALE', 'BD', 'ACCT', 'FIN')
      OR 
      js2.skill_abr IN ('IT', 'ENG', 'MGMT', 'ANLS', 'PRJM', 'SALE', 'BD', 'ACCT', 'FIN')
  )
GROUP BY js1.skill_abr, js2.skill_abr
ORDER BY pair_frequency DESC
LIMIT 50;
"""

print("Extracting 50 dense skill clusters for the hackathon presentation...")

with engine.connect() as conn:
    df = pd.read_sql(text(query), conn)

matrix_df = df.pivot(index='skill_a', columns='skill_b', values='pair_frequency').fillna(0)

plt.figure(figsize=(14, 11))

sns.heatmap(
    matrix_df, 
    annot=True, 
    fmt=".0f", 
    cmap="rocket_r", 
    linewidths=0.5,
    linecolor="#f0f0f0",
    cbar_kws={'label': 'Number of Combined Job Postings'}
)

plt.title("The Modern Job Ecosystem: Skill Co-occurrence Matrix", fontsize=18, fontweight='bold', pad=25)
plt.xlabel("Skill Category B", fontsize=13, labelpad=12, fontweight='semibold')
plt.ylabel("Skill Category A", fontsize=13, labelpad=12, fontweight='semibold')
plt.xticks(fontsize=11, rotation=45)
plt.yticks(fontsize=11, rotation=0)
plt.tight_layout()

output_path = "src/presentation_skill_clusters.png"
plt.savefig(output_path, dpi=300)
print(f"Presentation saved to: {output_path}")