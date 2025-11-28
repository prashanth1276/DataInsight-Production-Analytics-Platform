import sys
import os
import pandas as pd
import psycopg2
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import Config

class DataInsightETL:
    def __init__(self):
        self.connection_params = {
            'host': Config.DB_HOST,
            'port': Config.DB_PORT,
            'database': Config.DB_NAME,
            'user': Config.DB_USER,
            'password': Config.DB_PASSWORD
        }
    
    def create_connection(self):
        """Create direct PostgreSQL connection"""
        return psycopg2.connect(**self.connection_params)
    
    def extract(self, file_path):
        """Extract data from CSV"""
        print("Extracting data from CSV...")
        df = pd.read_csv(file_path)
        print(f"   Loaded {len(df):,} records")
        return df
    
    def transform(self, df):
        """Clean and transform the data"""
        print("Transforming data...")
        
        df['sales'] = df['Quantity'] * df['Price']
        
        df = df.rename(columns={
            'Invoice': 'order_id',
            'Description': 'product',
            'InvoiceDate': 'date',
            'Customer ID': 'customer_id'
        })
        
        df = df[['order_id', 'product', 'sales', 'date', 'customer_id', 'Country']]
        
        df = df.dropna()
        df['date'] = pd.to_datetime(df['date'])
        df = df[df['sales'] > 0]  # Remove negative sales
        
        print(f"   Transformed {len(df):,} valid sales records")
        return df
    
    def load(self, df):
        """Load data to PostgreSQL using direct connection"""
        print("Loading data to PostgreSQL...")
        
        conn = self.create_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DROP TABLE IF EXISTS sales_data;")
            cursor.execute("""
                CREATE TABLE sales_data (
                    id SERIAL PRIMARY KEY,
                    order_id VARCHAR(50),
                    product VARCHAR(255),
                    sales DECIMAL(10,2),
                    date TIMESTAMP,
                    customer_id VARCHAR(50),
                    country VARCHAR(50)
                );
            """)
            
            for index, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO sales_data (order_id, product, sales, date, customer_id, country)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (row['order_id'], row['product'], row['sales'], row['date'], row['customer_id'], row['Country']))
            
            conn.commit()
            print("   Data loaded successfully!")
            
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()
    
    def run_pipeline(self, file_path):
        """Run the complete ETL pipeline"""
        print("Starting ETL Pipeline...")
        start_time = datetime.now()
        
        raw_data = self.extract(file_path)
        transformed_data = self.transform(raw_data)
        self.load(transformed_data)
        
        processing_time = (datetime.now() - start_time).total_seconds()
        
        print(f"ETL completed in {processing_time:.2f} seconds")
        print(f"Final dataset: {len(transformed_data):,} sales records")
        
        return len(transformed_data)

# Run the pipeline
if __name__ == "__main__":
    try:
        etl = DataInsightETL()
        final_count = etl.run_pipeline('../Dataset/retail_15000.csv')
        print(f"\nSuccessfully processed {final_count:,} records!")
        
    except Exception as e:
        print(f"Pipeline failed: {e}")