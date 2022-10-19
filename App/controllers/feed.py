from App.database import db
from App.models import Profile
import json
from datetime import datetime
from dataclasses import dataclass
from dataclasses import dataclass
from dataclasses import asdict

def current_time_ms():
    '''Returns current time in miliseconds.'''
    return round(datetime.utcnow().timestamp() * 1000)

def refresh():
    filename = 'App/config/feed.json'
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











#  TIER STUFF
@dataclass
class Tier:
    tier: int
    tier_points: int
    views_left: int

tiers = {}

def define_tiers():
    tiers = {
        1: asdict(Tier(1,0,2)),
        2: asdict(Tier(2,4,4)),
        3: asdict(Tier(3,6,6)),
        4: asdict(Tier(4,8,8)),
        5: asdict(Tier(5,10,10))
    }

def determine_tier(tier_points: int):
    for key in tiers:
        if tier_points == tiers[key][tier_points]:
            return tiers[key]
    return {}























def get_all_profiles():
    return Profile.query.all()



def refresh_views():
    feed = Feed.query.first()
    if feed.refresh():
        profiles = get_all_profiles()
        if profiles:
            for profile in profiles:
                profile.reset_views_left()
                db.session.add(profile)
        db.session.add(feed)
        db.session.commit()
        return True
    return False


def generate_feed():
    feed = Feed.query.first()
    if not feed:
        create_feed();
        
    profiles = get_all_profiles()
    refresh_views()
    listing = []
    if profiles:
        for profile in profiles:
            if profile.views_left != None and profile.views_left > 0:
                listing.append(profile)
                profile.views_left -= 1
                db.session.add(profile)
        db.session.commit()
    return listing
