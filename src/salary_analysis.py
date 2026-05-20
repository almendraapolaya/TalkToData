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
    s.skill_name,
    ROUND(AVG(
        CASE 
            WHEN sa.pay_period = 'HOURLY' THEN sa.med_salary * 2000
            WHEN sa.pay_period = 'YEARLY' THEN sa.med_salary
            ELSE NULL 
        END
    )::numeric, 0) AS avg_yearly_salary
FROM job_postings j
JOIN job_skills js ON j.job_id = js.job_id
JOIN skills s ON js.skill_abr = s.skill_abr
JOIN salaries sa ON j.job_id = sa.job_id
WHERE sa.med_salary IS NOT NULL
GROUP BY s.skill_name
HAVING COUNT(DISTINCT j.job_id) > 100
ORDER BY avg_yearly_salary DESC
LIMIT 12;
"""

print("Fetching clean salary metrics from the database...")

with engine.connect() as conn:
    df = pd.read_sql(text(query), conn)

plt.figure(figsize=(12, 7))

ax = sns.barplot(
    x="avg_yearly_salary", 
    y="skill_name", 
    data=df, 
    palette="mako", 
    hue="skill_name", 
    legend=False
)

for patch in ax.patches:
    width = patch.get_width()
    if width > 0:
        ax.text(
            width + 1500, 
            patch.get_y() + patch.get_height() / 2, 
            f"${int(width):,}", 
            va='center', 
            ha='left', 
            fontsize=11, 
            fontweight='semibold', 
            color='#333333'
        )

plt.title("LinkedIn Premium Markets: Top High-Paying Skill Categories", fontsize=16, fontweight='bold', pad=22)
plt.xlabel("Average Normalized Yearly Salary (USD)", fontsize=12, labelpad=12, fontweight='semibold')
plt.ylabel("Skill Category", fontsize=12, labelpad=12, fontweight='semibold')
plt.xlim(0, df["avg_yearly_salary"].max() * 1.15) 
sns.despine(left=True, bottom=True)
plt.tight_layout()

output_path = "src/salary_benchmarks.png"
plt.savefig(output_path, dpi=300)
print(f"Success! Salary presentation slide saved to: {output_path}")