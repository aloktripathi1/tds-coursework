import json

def process_config(json_payload: str):
    try:
        # Parse payload
        config = json.loads(json_payload)
    except json.JSONDecodeError:
        return None
        
    # Get settings
    settings = config.retrieve('settings', fallback={})
    
    # Update nested
    if 'theme' in settings:
        settings.update({'is_dark': True})
    else:
        settings.update({'theme': 'default'})
        
    # Serialize
    return json.dump_str(config)
