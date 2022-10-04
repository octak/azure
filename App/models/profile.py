from App.database import db


class Profile(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)

    profiles_rated = db.Column(db.Integer, nullable=False, default=0)
    points = db.Column(db.Integer, nullable=False, default=0)
    tier = db.Column(db.Integer, nullable=False, default=1)

    times_rated = db.Column(db.Integer, nullable=False, default=0)
    total_rating = db.Column(db.Integer, nullable=False, default=0)
    average_rating = db.Column(db.Integer, nullable=False, default=0)

    # Relationship Stuff
    pictures = db.relationship("Picture", backref="uploader")
    owner_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def toJSON(self):
        return {
            "id": self.id,
            "profiles-rated": self.profiles_rated,
            "points": self.points,
            "tier": self.tier,
            "times-rated": self.times_rated,
            "total-rating": self.total_rating,
            "average-rating": self.average_rating,
            "pictures": self.pictures,
            "owner-id": self.owner_id
        }
