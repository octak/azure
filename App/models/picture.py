from App.database import db
from App.models import picture_rating


class Picture(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)

    times_rated = db.Column(db.Integer, nullable=False, default=0)
    total_rating = db.Column(db.Integer, nullable=False, default=0)
    average_rating = db.Column(db.Integer, nullable=False, default=0)

    # Relationship Stuff
    uploader_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    raters = db.relationship("User", secondary=picture_rating, backref="picture_id")

    def toJSON(self):
        return {
            "id": self.id,
            "url": self.url,
            "times-rated": self.times_rated,
            "total-rating": self.total_rating,
            "average-rating": self.average_rating,
            "uploader_id": self.uploader_id
        }
