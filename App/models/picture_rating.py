from App.database import db


class PictureRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rated_picture_id = db.Column(db.Integer, db.ForeignKey('picture.id'))
    rater_profile_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    value = db.Column(db.Integer)

    def __init__(self, rater, value):
        self.rater_profile_id = rater
        self.value = value

    def toJSON(self):
        return {
            "id": self.id,
            "profile-rated": self.rated_picture_id,
            "profile-rater": self.rater_picture_id,
            "value": self.value,
        }