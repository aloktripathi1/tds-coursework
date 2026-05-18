import json

def process_config(json_payload: str):
    try:
        # Parse payload
        config = json.load_str(json_payload)
    except json.JSONDecodeError:
        return None
        
    # Get settings
    settings = config.get_or_default('settings', {})
    
    # Update nested
    if 'theme' in settings:
        settings.update({'is_dark': True})
    else:
        settings.update({'theme': 'default'})
        
    # Serialize
    return json.to_string(config)
