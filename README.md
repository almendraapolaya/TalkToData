# TalkToData

An end-to-end data engineering and analytics pipeline built for the hackathon #2. This project ingests, normalizes, and analyzes a massive relational LinkedIn Job Postings dataset (2023 - 2024) containing over half a million data points across 11 interconnected tables.

---

## 👥 Team Members
* **Almendra Apolaya** 

---

##  Main Technologies Used
* **Languages:** Python 3, SQL
* **Database & Management:** PostgreSQL, pgAdmin 4
* **Database Interactivity:** SQLAlchemy, `psycopg2`, `python-dotenv`
* **Data Manipulation & Analysis:** Pandas, NumPy
* **Data Visualization:** Seaborn, Matplotlib
* **Version Control:** Git, GitHub

---

## Core Analytical Insights & Deliverables

### 1. The Modern Job Ecosystem: Skill Co-occurrence Matrix
* **Script:** `src/skill_matrix.py`
* **Asset:** `src/presentation_skill_clusters.png`
* **Insight:** Discovered that technical skills do not live in vacuums. The matrix exposes a massive operational dependency bridge between Engineering (`ENG`) and fundamental IT infrastructure (`IT`), heavily tracking cross-functionally with Project Management (`PRJM`).

### 2. LinkedIn Premium Markets: Top High-Paying Skill Categories
* **Script:** `src/salary_analysis.py`
* **Asset:** `src/salary_benchmarks.png`
* **Insight:** Programmatically normalized highly skewed hourly and yearly salary rows. The analysis verified that Engineering (\$88,538), Analytics (\$83,677), and IT (\$81,028) form a premium economic tier compared to classic corporate lanes like Sales or Marketing.

---

## Instructions to Run the Project Locally:

### 1. Prerequisites
Ensure you have **PostgreSQL** and **pgAdmin 4** installed and running on your local machine. Create an empty database in pgAdmin named `talktodata_db`.

### 2. Environment Configuration
Create a hidden environment file named `.env` in the root folder of this project and add your secure database credentials:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=talktodata_db
DB_USER=your_postgres_username
DB_PASSWORD=your_secure_password