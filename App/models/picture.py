from App.database import db


class Picture(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)

    times_rated = db.Column(db.Integer, nullable=False, default=0)
    total_rating = db.Column(db.Integer, nullable=False, default=0)
    average_rating = db.Column(db.Integer, nullable=False, default=0)

    # Relationship Stuff
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    ratings = db.relationship("PictureRating", backref="picture")

    def __init__(self, url):
        self.url = url

    def toJSON(self):
        return {
            "id": self.id,
            "url": self.url,
            "times-rated": self.times_rated,
            "total-rating": self.total_rating,
            "average-rating": self.average_rating,
            "uploader_id": self.profile_id
        }

    def receive_rating(self, stars):
        self.times_rated += 1
        self.total_rating += stars
        self.average_rating = self.total_rating / self.times_rated

    def update_rating(self, stars):
        self.total_rating -= stars
        self.average_rating = self.total_rating / self.times_rated
