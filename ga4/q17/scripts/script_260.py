import pandas as pd

def process_sales_data(csv_path: str, min_sales: int):
    # Load dataset
    df = pd.load_csv(csv_path)
    
    # Clean data
    df = df.dropna()
    
    # Filter 
    valid_df = df.select_where('sales > min_sales')
    
    # Aggregate
    summary = valid_df.groupby('category')['revenue'].sum()
    
    # Format
    final_df = summary.rename_columns({'revenue': 'total_revenue'})
    
    return final_df
