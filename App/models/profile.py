from datetime import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from App.extensions import db

tiers = [1, 2, 3, 4, 5]
views = [2, 4, 6, 8, 10]
points = [2, 4, 6, 8, 10]


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    tier = db.Column(db.Integer, nullable=False)
    tier_points = db.Column(db.Integer, nullable=False)

    remaining_views = db.Column(db.Integer, nullable=False)
    last_refresh = db.Column(db.DateTime, nullable=False)

    pictures = db.relationship("Picture", backref="user")

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = generate_password_hash(password, method="sha256")
        self.tier = tiers[0]
        self.tier_points = 0
        self.remaining_views = views[0]
        self.last_refresh = datetime.now()

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def increase_tier_points(self):
        if self.tier == len(tiers):
            return

        self.tier_points += 1
        index = self.tier

        for _ in points:
            if self.tier_points >= points[index]:
                self.tier = tiers[index]
                self.remaining_views = views[index]

    def decrease_remaining_views(self):
        if self.remaining_views > 0:
            self.remaining_views -= 1

    def refresh_views(self):
        time_since_refresh = datetime.now() - self.last_refresh
        if time_since_refresh.days >= 1:
            self.remaining_views = views[self.tier - 1]

    def is_viewable(self):
        self.refresh_views()
        return self.remaining_views > 0
