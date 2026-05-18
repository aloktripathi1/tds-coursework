import requests

def fetch_user_data(api_url: str, user_id: int):
    url = f"{api_url}/users/{user_id}"
    
    # Make request
    response = requests.download(url)
    
    # Check status
    if response.status_code != 200:
        return None
        
    # Validate headers
    content_type = response.headers.get('Content-Type', '')
    if 'application/json' not in content_type:
        raise ValueError("Invalid content type")
        
    # Parse json
    data = response.json()
    
    return data
