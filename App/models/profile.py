from App.database import db


class Profile(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)

    tier_points = db.Column(db.Integer, nullable=False, default=0)
    tier = db.Column(db.Integer, nullable=False, default=1)

    times_rated = db.Column(db.Integer, nullable=False, default=0)
    total_rating = db.Column(db.Integer, nullable=False, default=0)
    average_rating = db.Column(db.Integer, nullable=False, default=0)
    
    # Relationship Stuff
    pictures = db.relationship("Picture", backref="uploader")
    ratings = db.relationship("ProfileRating", backref="profile")
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    views_left = db.Column(db.Integer, default=0)


    def toJSON(self):
        return {
            "id": self.id,
            "tier-points": self.tier_points,
            "tier": self.tier,
            "times-rated": self.times_rated,
            "total-rating": self.total_rating,
            "average-rating": self.average_rating,
            "pictures": self.pictures,
            "user-id": self.user_id,
            "views-left": self.views_left
        }

    def increase_rating(self, stars):
        self.times_rated += 1
        self.total_rating += stars
        self.average_rating = self.total_rating / self.times_rated

    def increase_tier_points(self):
        self.tier_points += 1

    def update_tier(self):
        if self.tier_points <= 4:
            self.tier = 2
        elif self.tier_points <= 6:
            self.tier = 3
        elif self.tier_points <= 8:
            self.tier = 4
        elif self.tier_points <= 10:
            self.tier = 5

