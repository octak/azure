from App.database import db
from werkzeug.security import check_password_hash, generate_password_hash


class Profile(db.Model):
    views_per_tier = {1: 2, 2: 4, 3: 6, 4: 8, 5: 10}

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    tier = db.Column(db.Integer, nullable=False, default=1)
    tier_points = db.Column(db.Integer, nullable=False, default=0)
    times_rated = db.Column(db.Integer, nullable=False, default=0)
    total_rating = db.Column(db.Integer, nullable=False, default=0)
    average_rating = db.Column(db.Integer, nullable=False, default=0)
    views_left = db.Column(db.Integer, default=views_per_tier[1])

    pictures = db.relationship("Picture", back_populates="profile")
    ratings = db.relationship("ProfileRating", backref="rater")
    picture_ratings = db.relationship("PictureRating", backref="rater")

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def serialize_pictures(self) -> dict:
        pictures = {}
        for _, picture in enumerate(self.pictures):
            pictures[_] = picture.serialize()
        return pictures

    def serialize(self) -> dict:
        return {
            "id": self.id,
            "username": self.username,
            "tier": self.tier,
            "average-rating": self.average_rating,
            "pictures": self.serialize_pictures()
        }

    def receive_rating(self, value):
        self.times_rated += 1
        self.total_rating += value
        self.average_rating = self.total_rating / self.times_rated

    def update_rating(self, value):
        self.total_rating -= value
        self.average_rating = self.total_rating / self.times_rated

    def upgrade_tier(self, tier_info):
        if tier_info:
            self.tier = tier_info['tier']
            self.tier_points = tier_info['tier_points']
            self.views_left =  tier_info['views_left']

    def add_tier_point(self):
        if self.tier_points < 10:
            self.tier_points += 1
            self.update_tier()