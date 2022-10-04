from App.database import db
from App.models import picture_rating, user_rating
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    # Relationship Stuff
    profiles = db.relationship("Profile", backref="owner")
    rated_pictures = db.relationship("Picture", secondary=picture_rating, backref="rater_id")
    rated_users = db.relationship("User", secondary=user_rating, backref="rater_id")

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def toJSON(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password
        }
