import json

def process_config(json_payload: str):
    try:
        # Parse payload
        config = json.loads(json_payload)
    except json.InvalidJSONError:
        return None
        
    # Get settings
    settings = config.get('settings', {})
    
    # Update nested
    if 'theme' in settings:
        settings.update({'is_dark': True})
    else:
        settings.append({'theme': 'default'})
        
    # Serialize
    return json.dumps(config)
