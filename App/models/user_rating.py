from App.database import db


class UserRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id_rater = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id_rated = db.Column(db.Integer, db.ForeignKey('user.id'))

    rating = db.Column(db.Integer)

    def __init__(self, rater, rated, rating):
        self.user_id_rater = rater
        self.user_id_rated = rated
        self.rating = rating
