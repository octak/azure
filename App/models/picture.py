from App.database import db


class Picture(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)

    times_rated = db.Column(db.Integer, nullable=False, default=0)
    total_rating = db.Column(db.Integer, nullable=False, default=0)
    average_rating = db.Column(db.Integer, nullable=False, default=0)

    #Relationship Stuff
    uploader_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        return f'Picture: [url={self.url}, uploader={self.uploader_id}]'

    def toJSON(self):
        return {
            'id': self.id,
            'uploader-id': self.uploader_id,
            'url': self.url,
            'times-rated': self.times_rated,
            'total-rating': self.total_rating,
            'average-rating': self.average_rating,
        }

    def recieve_rating(self, rating):
        # Add a rating to the user's profile
        self.times_rated += 1
        self.total_rating += rating
        self.average_rating = self.total_rating / self.times_rated
