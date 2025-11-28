from fastapi import APIRouter, HTTPException
from app.models.schemas import HealthResponse
from app.database import db
from datetime import datetime

router = APIRouter()

@router.get("/", response_model=HealthResponse)  # Changed from "/health" to "/"
def health_check():
    """Health check endpoint"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        
        return HealthResponse(
            status="healthy",
            database="connected",
            timestamp=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {e}")