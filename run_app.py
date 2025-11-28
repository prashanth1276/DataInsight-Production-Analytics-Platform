import uvicorn
from app.main import app

if __name__ == "__main__":
    print("Starting DataInsight API Server...")
    print("Local URL: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop the server")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=False,
        log_level="info"
    )