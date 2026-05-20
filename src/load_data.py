import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

connection_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(connection_url)

DATA_DIR = "/Users/emmyalmendra/Desktop/Code/LinkedIn Job Postings (2023 - 2024)"

print("Ingestion engine initialized. Ready to process tables...")

# --- LOADING A CSV TO POSTGRES ---

def load_table_to_db(file_path, table_name):
    print(f"Loading {table_name}...")
    try:
        df = pd.read_csv(file_path)
        df.to_sql(table_name, con=engine, if_exists="replace", index=False)
        print(f"Success! Loaded {len(df)} rows into table '{table_name}'.\n")
    except Exception as e:
        print(f"Failed to load {table_name}. Error: {e}\n")

def load_giant_table_to_db(file_path, table_name, chunk_size=10000):
    print(f"Loading giant table {table_name} in chunks of {chunk_size}...")
    try:
        first_chunk = True
        total_rows = 0
        
        for chunk in pd.read_csv(file_path, chunksize=chunk_size):
            if first_chunk:
                chunk.to_sql(table_name, con=engine, if_exists="replace", index=False)
                first_chunk = False
            else:
                chunk.to_sql(table_name, con=engine, if_exists="append", index=False)
            
            total_rows += len(chunk)
            print(f"   -> Progress: {total_rows} rows stream-loaded...")
            
        print(f"Success! Total of {total_rows} rows loaded into '{table_name}'.\n")
    except Exception as e:
        print(f"Failed to load giant table {table_name}. Error: {e}\n")

# --- INGESTION FOR LOOKUP TABLES ---
if __name__ == "__main__":
    print("--- STARTING DATA INGESTION --- \n")
    
    skills_path = f"{DATA_DIR}/mappings/skills.csv"
    load_table_to_db(skills_path, "skills")
    
    industries_path = f"{DATA_DIR}/mappings/industries.csv"
    load_table_to_db(industries_path, "industries")
    
    print("--- FIRST PHASE COMPLETE ---")

    salaries_path = f"{DATA_DIR}/jobs/salaries.csv"
    load_table_to_db(salaries_path, "salaries")
    
    benefits_path = f"{DATA_DIR}/jobs/benefits.csv"
    load_table_to_db(benefits_path, "benefits")
    
    companies_path = f"{DATA_DIR}/companies/companies.csv"
    load_table_to_db(companies_path, "companies")
    
    employee_counts_path = f"{DATA_DIR}/companies/employee_counts.csv"
    load_table_to_db(employee_counts_path, "employee_counts")
    
    print("--- SECOND PHASE COMPLETE ---")

    job_skills_path = f"{DATA_DIR}/jobs/job_skills.csv"
    load_table_to_db(job_skills_path, "job_skills")
    
    job_industries_path = f"{DATA_DIR}/jobs/job_industries.csv"
    load_table_to_db(job_industries_path, "job_industries")
    
    company_specialities_path = f"{DATA_DIR}/companies/company_specialities.csv"
    load_table_to_db(company_specialities_path, "company_specialities")
    
    company_industries_path = f"{DATA_DIR}/companies/company_industries.csv"
    load_table_to_db(company_industries_path, "company_industries")
    
    print("--- THIRD PHASE COMPLETE ---")

    postings_path = f"{DATA_DIR}/postings.csv"
    load_giant_table_to_db(postings_path, "job_postings")
    
    print("ALL DATA INGESTION COMPLETELY FINISHED!")