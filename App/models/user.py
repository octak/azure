from App.database import db
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    # Relationship Stuff
    profiles = db.relationship("Profile", backref="owner")

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)
