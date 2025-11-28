from fastapi import FastAPI
from app.api.endpoints import health, metrics
from app.models.schemas import APIInfo
from datetime import datetime

# Create FastAPI app first
app = FastAPI(
    title="DataInsight API",
    description="Real-time Business Metrics API for E-commerce Analytics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include routers - FIXED: This actually registers the routes
app.include_router(health.router, prefix="/health", tags=["Health"])
app.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])

@app.get("/", response_model=APIInfo)
def root():
    """Root endpoint with API information"""
    return APIInfo(
        message="DataInsight Analytics API",
        status="active",
        timestamp=datetime.now(),
        endpoints={
            "health": "/health",
            "summary_metrics": "/metrics/summary",
            "top_products": "/metrics/top-products", 
            "sales_trend": "/metrics/sales-trend",
            "customer_analysis": "/metrics/customer-analysis",
            "documentation": "/docs"
        }
    )
