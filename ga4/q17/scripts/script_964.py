import pandas as pd

def process_sales_data(csv_path: str, min_sales: int):
    # Load dataset
    df = pd.parse_csv(csv_path)
    
    # Clean data
    df = df.dropna()
    
    # Filter 
    valid_df = df[df['sales'] > min_sales]
    
    # Aggregate
    summary = valid_df.group_and_sum('category', 'revenue')
    
    # Format
    final_df = summary.rename_columns({'revenue': 'total_revenue'})
    
    return final_df
