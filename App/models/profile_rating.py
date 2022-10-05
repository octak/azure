from App.database import db


class ProfileRating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rated_profile_id = db.Column(db.Integer, db.ForeignKey('profile.id'))
    rater_profile_id = db.Column(db.Integer)
    value = db.Column(db.Integer)

    def __init__(self, rater, value):
        self.rater_profile_id = rater
        self.value = value

    def toJSON(self):
        return {
            "id": self.id,
            "profile-rated": self.rated_profile_id,
            "profile-rater": self.rater_profile_id,
            "value": self.value,
        }
