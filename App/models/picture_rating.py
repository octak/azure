from App.database import db


class PictureRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    picture_id = db.Column(db.Integer, db.ForeignKey('picture.id'))

    rating = db.Column(db.Integer)

    def __init__(self, rater, rated, rating):
        self.user_id_rater = rater
        self.user_id_rated = rated
        self.rating = rating
