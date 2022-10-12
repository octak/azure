from App.database import db


class PictureRating(db.Model):
    rater_id = db.Column(db.Integer, primary_key=True)
    ratee_id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)

    def toJSON(self):
        return {
            "rated-picture": self.ratee_id,
            "rated-by": self.rater_id,
            "value": self.value,
        }
