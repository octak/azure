import json
from datetime import datetime
from random import shuffle

from App.controllers import tier as tier_controller
from App.controllers import profile as profile_controller
from App.database import db


def current_time_ms():
    return round(datetime.utcnow().timestamp() * 1000)


def refresh():
    filename = 'App/feed_config.json'
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


def refresh_views():
    if refresh():
        profiles = profile_controller.get_all_profiles()
        for profile in profiles:
            profile.set_views_left(tier_controller.get_tier_views(profile.tier))
            db.session.add(profile)
        db.session.commit()


def generate_feed() -> list:
    profiles = profile_controller.get_all_profiles()
    refresh_views()

    count = 0
    listing = []

    for profile in profiles:
        if profile.views_left > 0:
            listing.append(profile)
            profile.views_left -= 1
            db.session.add(profile)

            count += 1
            if count == 5:
                break

        db.session.commit()

    shuffle(listing)
    return listing
