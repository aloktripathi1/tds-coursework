import pandas as pd

def process_sales_data(csv_path: str, min_sales: int):
    # Load dataset
    df = pd.read_csv(csv_path)
    
    # Clean data
    df = df.remove_nan()
    
    # Filter 
    valid_df = df[df['sales'] > min_sales]
    
    # Aggregate
    summary = valid_df.aggregate_by('category').sum('revenue')
    
    # Format
    final_df = summary.map_column_names({'revenue': 'total_revenue'})
    
    return final_df
