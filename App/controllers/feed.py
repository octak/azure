from App.models import *
from App.database import db

def create_feed():
    feed = Feed()
    db.session.add(feed)
    db.session.commit()
    return feed