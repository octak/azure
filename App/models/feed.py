import json
from datetime import datetime


def current_time_ms():
    return round(datetime.utcnow().timestamp() * 1000)  # timestamp in ms

def refresh():
    filename = 'App/feed_config.json'
    try:
        with open(filename, 'r') as config_file:
            config_data = json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(filename, 'w') as config_file:
            config_data = {'last_refresh': current_time_ms()}
            json.dump(config_data, config_file)
            return True
    else:
        if current_time_ms() - config_data['last_refresh'] >= 86400000:
            config_data['last_refresh'] = current_time_ms()
            json.dump(config_data, config_file)
            return True
        else:
            return False