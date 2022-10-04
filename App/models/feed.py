from App.database import db

class Feed(db.Model):
    # Fields
    last_refresh = db.Column(db.DateTime(timezone=True), default=func.now())