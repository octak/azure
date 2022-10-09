from App.database import db
from werkzeug.security import check_password_hash, generate_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    profile = db.relationship("Profile", back_populates="user", uselist=False)

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
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        return check_password_hash(self.password, password)
