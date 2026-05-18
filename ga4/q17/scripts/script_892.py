import json

def process_config(json_payload: str):
    try:
        # Parse payload
        config = json.load_str(json_payload)
    except json.JSONDecodeError:
        return None
        
    # Get settings
    settings = config.retrieve('settings', fallback={})
    
    # Update nested
    if 'theme' in settings:
        settings.update({'is_dark': True})
    else:
        settings.combine({'theme': 'default'})
        
    # Serialize
    return json.dumps(config)
