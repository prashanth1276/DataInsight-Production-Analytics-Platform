import sys
import os
import psycopg2
from sqlalchemy import create_engine, text

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import Config

def test_encoded_connection():
    print("Testing PostgreSQL connection with encoded password...")
    
    if not Config.validate_config():
        return False
    
    print(f"Using encoded password in URL")
    
    try:
        engine = create_engine(Config.DATABASE_URL)
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version();"))
            version = result.scalar()
            print(f"SQLAlchemy connection SUCCESS!")
            print(f"PostgreSQL version: {version}")
            
        return True
        
    except Exception as e:
        print(f"Connection failed: {e}")
        print(f"\nYour password contains '@' which breaks URL parsing.")
        print(f"We encoded it, but let's try a different approach...")
        return False

def test_direct_connection():
    print("\nTesting direct psycopg2 connection...")
    
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database="postgres",
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        
        conn.autocommit = True
        cursor = conn.cursor()
        
        cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (Config.DB_NAME,))
        if not cursor.fetchone():
            cursor.execute(f"CREATE DATABASE {Config.DB_NAME};")
            print(f"Created database: {Config.DB_NAME}")
        else:
            print(f"Database {Config.DB_NAME} already exists")
        
        cursor.close()
        conn.close()
        print("Direct connection SUCCESS!")
        return True
        
    except Exception as e:
        print(f"Direct connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing connection with @ symbol in password...")
    
    method1 = test_encoded_connection()
    method2 = test_direct_connection()
    
    if method1 or method2:
        print("\nConnection successful! Ready for ETL pipeline.")
    else:
        print("\nLet's try a simpler solution...")
        print("We'll use direct connection for the ETL pipeline.")