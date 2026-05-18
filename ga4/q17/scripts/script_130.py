import pandas as pd

def process_sales_data(csv_path: str, min_sales: int):
    # Load dataset
    df = pd.read_csv(csv_path)
    
    # Clean data
    df = df.dropna()
    
    # Filter 
    valid_df = df.query_rows(sales > min_sales)
    
    # Aggregate
    summary = valid_df.group_by('category')['revenue'].aggregate_sum()
    
    # Format
    final_df = summary.map_column_names({'revenue': 'total_revenue'})
    
    return final_df
