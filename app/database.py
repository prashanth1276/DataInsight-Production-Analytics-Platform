import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
import os
import sys

# Add utils to path to import config
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from utils.config import Config

class DatabaseConnection:
    def __init__(self):
        self.config = {
            'host': Config.DB_HOST,
            'port': Config.DB_PORT,
            'database': Config.DB_NAME,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD
        }
        self.engine = create_engine(Config.DATABASE_URL)
    
    def get_connection(self):
        """Get database connection"""
        try:
            conn = psycopg2.connect(**self.config, cursor_factory=RealDictCursor)
            return conn
        except Exception as e:
            print(f"Database connection failed: {e}")
            raise
    
    def get_engine(self):
        """Get SQLAlchemy engine for pandas"""
        return self.engine

# Create database instance
db = DatabaseConnection()