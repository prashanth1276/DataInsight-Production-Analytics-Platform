import pandas as pd

df = pd.read_csv('../Dataset/retail_15000.csv')

print(f"Records: {len(df):,}")
print(f"Columns: {df.columns.tolist()}")

print("First 3 Rows: ")
print(df.head(3))