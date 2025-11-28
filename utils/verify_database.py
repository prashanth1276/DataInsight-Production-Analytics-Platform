import psycopg2
import pandas as pd
from utils.config import Config

def verify_database():
    print("Verifying database and data...")
    
    try:
        conn = psycopg2.connect(
            host=Config.DB_HOST,
            port=Config.DB_PORT,
            database=Config.DB_NAME,
            user=Config.DB_USER,
            password=Config.DB_PASSWORD
        )
        
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_name = 'sales_data'
        """)
        
        if not cursor.fetchone():
            print(" Table 'sales_data' does not exist!")
            return False
        
        cursor.execute("SELECT COUNT(*) FROM sales_data")
        record_count = cursor.fetchone()[0]
        print(f" Table 'sales_data' exists with {record_count:,} records")
        
        cursor.execute("SELECT * FROM sales_data LIMIT 3")
        sample_rows = cursor.fetchall()
        
        print("\n Sample data (first 3 rows):")
        print("ID | Order ID | Product | Sales | Date | Customer ID | Country")
        print("-" * 80)
        for row in sample_rows:
            print(f"{row[0]} | {row[1]} | {row[2][:20]}... | ${row[3]} | {row[4]} | {row[5]} | {row[6]}")
        
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT order_id) as unique_orders,
                COUNT(DISTINCT customer_id) as unique_customers,
                COUNT(DISTINCT product) as unique_products,
                SUM(sales) as total_sales,
                AVG(sales) as avg_sale
            FROM sales_data
        """)
        
        metrics = cursor.fetchone()
        print(f"\n Key Business Metrics:")
        print(f"   Unique Orders: {metrics[0]:,}")
        print(f"   Unique Customers: {metrics[1]:,}")
        print(f"   Unique Products: {metrics[2]:,}")
        print(f"   Total Sales: ${metrics[3]:,.2f}")
        print(f"   Average Sale: ${metrics[4]:.2f}")
        
        cursor.close()
        conn.close()
        
        print("\nDatabase verification completed successfully!")
        return True
        
    except Exception as e:
        print(f"Verification failed: {e}")
        return False

if __name__ == "__main__":
    verify_database()