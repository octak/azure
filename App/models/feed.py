from datetime import date, datetime, timedelta

from App.database import db


class Feed(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    last_refresh = db.Column(db.DateTime(timezone=True), default=datetime.now())

    def toJSON(self):
        return {
            "last-refresh": self.last_refresh,
            "current-time": datetime.now()
        }

    def refresh():
        current_time = datetime().now
        time_since_last_refresh = current_time - self.last_refresh

        if time_since_last_refresh.days >= 1:
            self.last_refresh = current_time
            return True
        return False
