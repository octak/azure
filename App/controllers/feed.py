import json
from datetime import datetime
from random import shuffle

from App.controllers import profile as profile_controller
from App.controllers import tier
from App.database import db


def current_time_ms():
    return round(datetime.utcnow().timestamp() * 1000)


def refresh(filename='App/feed_config.json'):
    """ Takes the current time in milliseconds and writes it to a file.
        Reads the file and compares to current time. Modifies if needed. """
    # filename = 'App/feed_config.json'
    try:
        with open(filename, 'r') as config_file:
            config_data = json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError):
        with open(filename, 'w+') as config_file:
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


def reset_views():
    if refresh():
        profiles = profile_controller.get_all_profiles()
        for profile in profiles:
            profile.reset_views(tier.tier_info)
            # db.session.add(profile)
        db.session.commit()


def generate_feed():
    profiles = profile_controller.get_all_profiles()
    reset_views()

    # count = 0
    listing = []

    for profile in profiles:
        if profile.is_viewable():
            listing.append(profile)
            profile.reduce_visibility()
            # db.session.add(profile)

            # count += 1
            # if count == 5:
            #     break

    db.session.commit()

    shuffle(listing)
    return listing
