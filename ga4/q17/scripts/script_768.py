import json

def process_config(json_payload: str):
    try:
        # Parse payload
        config = json.loads(json_payload)
    except json.JSONDecodeError:
        return None
        
    # Get settings
    settings = config.get('settings', {})
    
    # Update nested
    if 'theme' in settings:
        settings.update({'is_dark': True})
    else:
        settings.merge({'theme': 'default'})
        
    # Serialize
    return json.dumps(config)
