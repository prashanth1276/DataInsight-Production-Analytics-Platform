import sys
import os
import pandas as pd
import psycopg2
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import Config
import io

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
        df = df[df['sales'] > 0]
        
        print(f"   Transformed {len(df):,} valid sales records")
        return df
    
    def load_optimized(self, df):
        """Load data to PostgreSQL using COPY for maximum speed"""
        print("Loading data to PostgreSQL (optimized)...")
        
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
        
            output = io.StringIO()
            df.to_csv(output, sep='\t', header=False, index=False)
            output.seek(0)
            
            cursor.copy_from(output, 'sales_data', null="", 
                           columns=['order_id', 'product', 'sales', 'date', 'customer_id', 'country'])
            
            conn.commit()
            print("   Data loaded successfully with optimized method!")
            
        except Exception as e:
            conn.rollback()
            print(f"   COPY method failed, trying batch insert...")
            self.load_batch(df, conn)
        finally:
            cursor.close()
            conn.close()
    
    def load_batch(self, df, conn):
        """Batch insert as fallback"""
        cursor = conn.cursor()
        try:
            data_tuples = [tuple(row) for row in df.to_numpy()]
            
            cursor.executemany("""
                INSERT INTO sales_data (order_id, product, sales, date, customer_id, country)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, data_tuples)
            
            conn.commit()
            print("   Data loaded successfully with batch insert!")
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
    
    def run_pipeline(self, file_path):
        """Run the complete ETL pipeline"""
        print("Starting ETL Pipeline...")
        start_time = datetime.now()
        
        raw_data = self.extract(file_path)
        transformed_data = self.transform(raw_data)
        self.load_optimized(transformed_data)
        
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