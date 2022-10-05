from App.database import db
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(100))

    # Relationship Stuff
    profile = db.relationship("Profile", backref="owner", uselist=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def toJSON(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
        # self.password = password

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
