from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime

class HealthResponse(BaseModel):
    status: str
    database: str
    timestamp: datetime

class PerformanceMetrics(BaseModel):
    response_time_ms: float
    timestamp: datetime

class SummaryMetrics(BaseModel):
    total_records: int
    total_orders: int
    total_customers: int
    total_products: int
    total_sales: float
    average_sale_value: float
    maximum_sale: float
    minimum_sale: float

class SummaryResponse(BaseModel):
    metrics: SummaryMetrics
    performance: PerformanceMetrics

class ProductMetrics(BaseModel):
    product: str
    total_revenue: float
    sales_count: int
    unique_customers: int

class TopProductsResponse(BaseModel):
    top_products: List[ProductMetrics]
    performance: PerformanceMetrics

class SalesTrendItem(BaseModel):
    period: str
    total_sales: float
    transaction_count: int

class SalesTrendResponse(BaseModel):
    sales_trend: List[SalesTrendItem]
    timestamp: datetime

class CustomerAnalysis(BaseModel):
    total_customers: int
    average_customer_value: float
    max_customer_value: float

class TopCustomer(BaseModel):
    customer_id: str
    total_spent: float
    order_count: int

class CustomerAnalysisResponse(BaseModel):
    customer_analysis: CustomerAnalysis
    top_customers: List[TopCustomer]
    timestamp: datetime

class APIInfo(BaseModel):
    message: str
    status: str
    timestamp: datetime
    endpoints: Dict[str, str]