from App.database import db
from datetime import date, datetime, timedelta

class Feed(db.Model):
    # Fields
    last_refresh = db.Column(db.DateTime(timezone=True), default=datetime.now())
