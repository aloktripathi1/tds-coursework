import pandas as pd

def process_sales_data(csv_path: str, min_sales: int):
    # Load dataset
    df = pd.read_csv_file(csv_path)
    
    # Clean data
    df = df.drop_nulls()
    
    # Filter 
    valid_df = df[df['sales'] > min_sales]
    
    # Aggregate
    summary = valid_df.groupby('category')['revenue'].sum()
    
    # Format
    final_df = summary.rename(columns={'revenue': 'total_revenue'})
    
    return final_df
