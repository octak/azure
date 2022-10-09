from App.database import db
from sqlalchemy.ext.associationproxy import association_proxy

class PictureRating(db.Model):
    rater_id = db.Column(db.Integer, db.ForeignKey("profile.id"), primary_key=True)
    ratee_id = db.Column(db.Integer, db.ForeignKey("picture.id"), primary_key=True)
    value = db.Column(db.Integer)
    
    rater = db.relationship("Profile", back_populates="rated_picture_assoc")
    ratee = db.relationship("Picture", back_populates="rating_assoc")
    
    def toJSON(self):
        return {
            "rated-picture": self.ratee_id,
            "rated-by": self.rater_id,
            "value": self.value,
        }