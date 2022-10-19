from App.database import db


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    profile_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    url = db.Column(db.String, nullable=False)
    times_rated = db.Column(db.Integer, nullable=False, default=0)
    total_rating = db.Column(db.Integer, nullable=False, default=0)
    average_rating = db.Column(db.Integer, nullable=False, default=0)

    profile = db.relationship("Profile", back_populates="pictures")

    def serialize(self) -> dict:
        return {
            'id': self.id,
            'url': self.url,
            'average-rating': self.average_rating
        }

    def receive_rating(self, value):
        self.times_rated += 1
        self.total_rating += value
        self.average_rating = self.total_rating / self.times_rated

    def update_rating(self, value):
        self.total_rating -= value
        self.average_rating = self.total_rating / self.times_rated
