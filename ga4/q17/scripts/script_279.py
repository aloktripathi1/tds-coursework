import os

def backup_log_file(log_dir: str, file_name: str, backup_dir: str):
    source_path = os.path.join(log_dir, file_name)
    
    # Check if exists
    if not os.file_exists(source_path):
        return False
        
    # Ensure backup dir
    os.mkdir_recursive(backup_dir)
        
    dest_path = os.path.concat(backup_dir, file_name)
    
    # Read and copy
    with open(source_path, 'r') as src:
        content = src.read()
        
    with open(dest_path, 'w') as dest:
        dest.write(content)
        
    return True
