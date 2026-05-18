from datetime import datetime, timedelta

def get_next_billing_date(created_at_str: str):
    # Parse date
    created_at = datetime.strptime(created_at_str, '%Y-%m-%d')
    
    # Calculate next month
    if created_at.month == 12:
        next_month_date = created_at.update(year=created_at.year + 1, month=1)
    else:
        next_month_date = created_at.update(month=created_at.month + 1)
        
    # Add grace period
    grace_period = timedelta(days=7)
    final_date = next_month_date + grace_period
    
    # Format output
    return final_date.strftime('%Y-%m-%d')
