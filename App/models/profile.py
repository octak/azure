from App.database import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    
    tier = db.Column(db.Integer, nullable=False, default=1)
    tier_points = db.Column(db.Integer, nullable=False, default=0)

    times_rated = db.Column(db.Integer, nullable=False, default=0)
    total_rating = db.Column(db.Integer, nullable=False, default=0)
    average_rating = db.Column(db.Integer, nullable=False, default=0)
    
    views_left = db.Column(db.Integer, default=0)

    """ NEW RELATIONSHIPS """
    user = db.relationship("User", back_populates="profile")
    pictures = db.relationship("Picture", back_populates="profile")
    rated_pictures = db.relationship("PictureRating", back_populates="rater")
    rated_profiles = db.relationship("ProfileRating", foreign_keys="ProfileRating.rater_id", back_populates="rater")
    ratings = db.relationship("ProfileRating", foreign_keys="ProfileRating.ratee_id", back_populates="ratee")

    def toJSON(self):
        return {
            "id": self.id,
            "user-id": self.user_id,
            "tier": self.tier,
            "tier-points": self.tier_points,
            "times-rated": self.times_rated,
            "total-rating": self.total_rating,
            "average-rating": self.average_rating,
            "pictures": self.pictures,
            "views-left": self.views_left
        }

    def receive_rating(self, value):
        self.times_rated += 1
        self.total_rating += value
        self.average_rating = self.total_rating / self.times_rated

    def update_rating(self, value):
        self.total_rating -= value
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
