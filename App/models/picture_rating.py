from App.extensions import db


class PictureRating(db.Model):
    rater_id = db.Column(db.Integer, db.ForeignKey("profile.id"), primary_key=True)
    rated_id = db.Column(db.Integer, db.ForeignKey("picture.id"), primary_key=True)
    value = db.Column(db.Integer, nullable=False)

    rater = db.relationship("Profile", foreign_keys=[rater_id])
    rated = db.relationship("Picture", foreign_keys=[rated_id])
