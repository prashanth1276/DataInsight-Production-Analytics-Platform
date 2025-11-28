import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()

class Config:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '5432')
    DB_NAME = os.getenv('DB_NAME', 'datainsight')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    
    # URL encode the password to handle special characters
    ENCODED_PASSWORD = quote_plus(DB_PASSWORD) if DB_PASSWORD else ""
    
    DATABASE_URL = f"postgresql://{DB_USER}:{ENCODED_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate_config(cls):
        """Validate that all required environment variables are set"""
        if not cls.DB_PASSWORD:
            print("ERROR: DB_PASSWORD is not set in .env file!")
            return False
        
        required_vars = ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER']
        missing = [var for var in required_vars if not os.getenv(var)]
        
        if missing:
            print(f"Missing environment variables: {', '.join(missing)}")
            return False
            
        print("All environment variables are set correctly!")
        print(f"Password encoded for URL safety")
        return True

if __name__ == "__main__":
    print("Testing configuration...")
    if Config.validate_config():
        print(f"Database: {Config.DB_NAME}")
        print(f"User: {Config.DB_USER}")
        print(f"Host: {Config.DB_HOST}:{Config.DB_PORT}")
        print("Configuration is ready!")
    else:
        print("Configuration validation failed!")