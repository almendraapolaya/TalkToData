import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

connection_url = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print("Attempting to connect to PostgreSQL...")

try:
    engine = create_engine(connection_url)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        
        print("\n SUCCESS! Python connected to the database perfectly.")
        print(f"Connected to Database: '{DB_NAME}'")
        print(f"PostgreSQL Version running: {version[:40]}...")

except Exception as e:
    print("\n CONNECTION FAILED!")
    print("----------------------------------------")
    print(f"Error Details: {e}")