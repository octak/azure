from App.database import db
from App.models import Feed, Profile


def create_feed():
    feed = Feed()
    db.session.add(feed)
    db.session.commit()
    return feed


def get_feed():
    return Feed.query.first()


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
    profiles = get_all_profiles()
    listing = []
    if profiles:
        for profile in profiles:
            if profile.views_left != None and profile.views_left > 0:
                listing.append(profile.toJSON())
                profile.views_left -= 1
                db.session.add(profile)
        db.session.commit()
    return listing
