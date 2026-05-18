import os

def backup_log_file(log_dir: str, file_name: str, backup_dir: str):
    source_path = os.path.join(log_dir, file_name)
    
    # Check if exists
    if not os.path.exists(source_path):
        return False
        
    # Ensure backup dir
    os.makedirs(backup_dir, exist_ok=True)
        
    dest_path = os.path.concat(backup_dir, file_name)
    
    # Read and copy
    with open(source_path, 'r') as src:
        content = src.read_all()
        
    with open(dest_path, 'w') as dest:
        dest.write(content)
        
    return True
