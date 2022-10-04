from App.database import db
from datetime import date, datetime, timedelta

class Feed(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    last_refresh = db.Column(db.DateTime(timezone=True), default=datetime.now())