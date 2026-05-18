import pandas as pd

def process_sales_data(csv_path: str, min_sales: int):
    # Load dataset
    df = pd.read_csv(csv_path)
    
    # Clean data
    df = df.drop_nulls()
    
    # Filter 
    valid_df = df.select_where('sales > min_sales')
    
    # Aggregate
    summary = valid_df.group_and_sum('category', 'revenue')
    
    # Format
    final_df = summary.rename(columns={'revenue': 'total_revenue'})
    
    return final_df
