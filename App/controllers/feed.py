from App.models import *
from App.database import db
from App.controllers import get_all_profiles

def create_feed():
    feed = Feed()
    db.session.add(feed)
    db.session.commit()
    return feed

def get_feed():
    return Feed.query.first() 

def refresh_views():
    feed = Feed.query.first() 
    feed.refresh_views()

def generate_feed():
    profiles = get_all_profiles()
    listing = []
    for profile in profiles:
        if profile.views_left != None and profile.views_left > 0:
            listing.append(profile.toJSON())
            profile.views_left -= 1
            db.session.add(profile)
    db.session.commit()
    return listing
            