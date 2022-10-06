from datetime import date, datetime, timedelta

from App.database import db


class Feed(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    last_refresh = db.Column(db.DateTime(timezone=True), default=datetime.now())

    tier_view_dict = {
        "1": 2,
        "2": 4,
        "3": 6,
        "4": 8,
        "5": 10
    }


    def toJSON(self):
        return {
            "last-refresh": self.last_refresh,
            "current-time": datetime.now()
        }

    def refresh(self):
        current_time = datetime.now()
        time_since_last_refresh = current_time - self.last_refresh

        if time_since_last_refresh.days >= 1:
            self.last_refresh = current_time
            return True
        return False
