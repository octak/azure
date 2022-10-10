from App.database import db


class ProfileRating(db.Model):
    rater_id = db.Column(db.Integer, db.ForeignKey("profile.id"), primary_key=True)
    ratee_id = db.Column(db.Integer, db.ForeignKey("profile.id"), primary_key=True)
    value = db.Column(db.Integer)

    rater = db.relationship("Profile", foreign_keys=[rater_id], back_populates="rated_profile_assoc")
    ratee = db.relationship("Profile", foreign_keys=[ratee_id], back_populates="rating_assoc")

    def toJSON(self):
        return {
            "rated-profile": self.ratee_id,
            "rated-by": self.rater_id,
            "value": self.value,
        }
