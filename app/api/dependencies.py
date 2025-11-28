import time
from datetime import datetime
from typing import Dict, Any
from app.database import db

def get_db_connection():
    """Dependency for database connection"""
    return db.get_connection()

def measure_performance() -> Dict[str, Any]:
    """Measure API performance"""
    start_time = time.time()
    
    def calculate_performance():
        response_time = (time.time() - start_time) * 1000
        return {
            "response_time_ms": round(response_time, 2),
            "timestamp": datetime.now()
        }
    
    return calculate_performance