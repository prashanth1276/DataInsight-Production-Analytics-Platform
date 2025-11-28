from fastapi import APIRouter, Depends, HTTPException
import pandas as pd
from app.models.schemas import (
    SummaryResponse, SummaryMetrics, PerformanceMetrics,
    TopProductsResponse, ProductMetrics,
    SalesTrendResponse, SalesTrendItem,
    CustomerAnalysisResponse, CustomerAnalysis, TopCustomer
)
from app.api.dependencies import get_db_connection, measure_performance
from datetime import datetime
from app.database import db

router = APIRouter()

@router.get("/summary", response_model=SummaryResponse)
def get_summary_metrics(
    conn = Depends(get_db_connection),
    performance_measure=Depends(measure_performance)
):
    """Get key business metrics summary"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                COUNT(*) as total_records,
                COUNT(DISTINCT order_id) as total_orders,
                COUNT(DISTINCT customer_id) as total_customers,
                COUNT(DISTINCT product) as total_products,
                SUM(sales) as total_sales,
                AVG(sales) as avg_sale_value,
                MAX(sales) as max_sale,
                MIN(sales) as min_sale
            FROM sales_data
        """)
        
        result = cursor.fetchone()
        cursor.close()
        
        metrics = SummaryMetrics(
            total_records=result['total_records'],
            total_orders=result['total_orders'],
            total_customers=result['total_customers'],
            total_products=result['total_products'],
            total_sales=float(result['total_sales']) if result['total_sales'] else 0,
            average_sale_value=float(result['avg_sale_value']) if result['avg_sale_value'] else 0,
            maximum_sale=float(result['max_sale']) if result['max_sale'] else 0,
            minimum_sale=float(result['min_sale']) if result['min_sale'] else 0
        )
        
        return SummaryResponse(
            metrics=metrics,
            performance=performance_measure()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching metrics: {e}")

@router.get("/top-products", response_model=TopProductsResponse)
def get_top_products(
    limit: int = 10,
    conn = Depends(get_db_connection),
    performance_measure=Depends(measure_performance)
):
    """Get top selling products by revenue"""
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                product,
                SUM(sales) as total_revenue,
                COUNT(*) as sales_count,
                COUNT(DISTINCT customer_id) as unique_customers
            FROM sales_data
            GROUP BY product
            ORDER BY total_revenue DESC
            LIMIT %s
        """, (limit,))
        
        products = []
        for row in cursor.fetchall():
            products.append(ProductMetrics(
                product=row['product'],
                total_revenue=float(row['total_revenue']),
                sales_count=row['sales_count'],
                unique_customers=row['unique_customers']
            ))
        
        cursor.close()
        
        return TopProductsResponse(
            top_products=products,
            performance=performance_measure()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching top products: {e}")

@router.get("/sales-trend", response_model=SalesTrendResponse)
def get_sales_trend():
    """Get sales trend over time (monthly)"""
    try:
        engine = db.get_engine()
        df = pd.read_sql("""
            SELECT date, sales 
            FROM sales_data 
            ORDER BY date
        """, engine)
        
        df['date'] = pd.to_datetime(df['date'])
        df['year_month'] = df['date'].dt.to_period('M')
        
        monthly_sales = df.groupby('year_month')['sales'].agg(['sum', 'count']).reset_index()
        monthly_sales['year_month'] = monthly_sales['year_month'].astype(str)
        
        trend_data = []
        for _, row in monthly_sales.iterrows():
            trend_data.append(SalesTrendItem(
                period=row['year_month'],
                total_sales=float(row['sum']),
                transaction_count=int(row['count'])
            ))
        
        return SalesTrendResponse(
            sales_trend=trend_data,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching sales trend: {e}")

@router.get("/customer-analysis", response_model=CustomerAnalysisResponse)
def get_customer_analysis(conn = Depends(get_db_connection)):
    """Get customer behavior analysis"""
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT customer_id) as total_customers,
                AVG(total_spent) as avg_customer_value,
                MAX(total_spent) as max_customer_value
            FROM (
                SELECT 
                    customer_id,
                    SUM(sales) as total_spent,
                    COUNT(DISTINCT order_id) as order_count
                FROM sales_data
                GROUP BY customer_id
            ) customer_stats
        """)
        
        customer_metrics = cursor.fetchone()
        
        cursor.execute("""
            SELECT 
                customer_id,
                SUM(sales) as total_spent,
                COUNT(DISTINCT order_id) as order_count
            FROM sales_data
            GROUP BY customer_id
            ORDER BY total_spent DESC
            LIMIT 5
        """)
        
        top_customers = []
        for row in cursor.fetchall():
            top_customers.append(TopCustomer(
                customer_id=str(row['customer_id']),
                total_spent=float(row['total_spent']),
                order_count=row['order_count']
            ))
        
        cursor.close()
        
        analysis = CustomerAnalysis(
            total_customers=customer_metrics['total_customers'],
            average_customer_value=float(customer_metrics['avg_customer_value']) if customer_metrics['avg_customer_value'] else 0,
            max_customer_value=float(customer_metrics['max_customer_value']) if customer_metrics['max_customer_value'] else 0
        )
        
        return CustomerAnalysisResponse(
            customer_analysis=analysis,
            top_customers=top_customers,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching customer analysis: {e}")