from werkzeug.security import check_password_hash, generate_password_hash

from App.database import db


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    tier = db.Column(db.Integer, nullable=False, default=1)
    tier_points = db.Column(db.Integer, nullable=False, default=0)
    times_rated = db.Column(db.Integer, nullable=False, default=0)
    total_rating = db.Column(db.Integer, nullable=False, default=0)
    average_rating = db.Column(db.Integer, nullable=False, default=0)
    views_left = db.Column(db.Integer, default=0)

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

    def add_tier_point(self):
        if self.tier_points < 10:
            self.tier_points += 1

    def set_tier(self, tier):
        self.tier = tier

    def set_views_left(self, views_left):
        self.views_left = views_left
