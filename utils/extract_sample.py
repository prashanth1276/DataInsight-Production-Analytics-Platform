import pandas as pd

df = pd.read_csv('Dataset/online_retail.csv')

sample_df = df.head(15000)

sample_df.to_csv('Dataset/retail_15000.csv', index=False)

print(f"Created sample with {len(sample_df)} records.")
print(f"File Size: {df.memory_usage(deep=True).sum()/1024/1024:.2f} MB.")
print(f"File Size: {sample_df.memory_usage(deep=True).sum()/1024/1024:.2f} MB.")