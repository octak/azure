from App.database import db


class PictureRating(db.Model):
    rater_id = db.Column(db.Integer, primary_key=True)
    ratee_id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
