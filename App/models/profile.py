from werkzeug.security import check_password_hash, generate_password_hash

from App.database import db


class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    times_rated = db.Column(db.Integer, nullable=False, default=0)
    total_rating = db.Column(db.Integer, nullable=False, default=0)
    average_rating = db.Column(db.Integer, nullable=False, default=0)

    tier = db.Column(db.Integer, nullable=False, default=1)
    tier_points = db.Column(db.Integer, nullable=False, default=0)
    remaining_views = db.Column(db.Integer, nullable=False, default=0)

    pictures = db.relationship("Picture", back_populates="profile")
    profile_ratings = db.relationship("ProfileRating", backref="rater")
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
            "average_rating": self.average_rating,
            "pictures": self.serialize_pictures()
        }

    def update_rating(self, value: int, is_new: bool):
        if is_new:
            self.times_rated += 1
        self.total_rating += value
        self.average_rating = self.total_rating / self.times_rated

    def add_tier_point(self, tier_info: dict):
        if self.tier < len(tier_info):
            self.tier_points += 1
            next_tier = self.tier + 1
            if self.tier_points == tier_info[next_tier][0]:
                self.tier = next_tier
                self.reset_views(tier_info)

    def reset_views(self, tier_info: dict):
        self.remaining_views = tier_info[self.tier][1]

    def is_viewable(self):
        return self.remaining_views > 0

    def reduce_visibility(self):
        self.remaining_views -= 1

    def update_username(self, username):
        self.username = username
