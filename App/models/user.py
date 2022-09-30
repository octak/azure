from App.database import db
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    profiles_rated = db.Column(db.Integer, nullable=False, default=0)
    points = db.Column(db.Integer, nullable=False, default=0)
    tier = db.Column(db.Integer, nullable=False, default=1)

    times_rated = db.Column(db.Integer, nullable=False, default=0)
    total_rating = db.Column(db.Integer, nullable=False, default=0)
    average_rating = db.Column(db.Integer, nullable=False, default=0)

    # Relationship Stuff
    pictures = db.relationship("Picture", backref="uploader")

    # Profile visibility information could possibly be stored in another table?
    remaining_views = db.Column(db.Integer, nullable=False, default=10)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def __repr__(self):
        return f'[user={self.username}, pass={self.password}, p_rated={self.profiles_rated}, points={self.points}, tier={self.tier}, t_rated={self.times_rated}, stars={self.total_rating}, avg_rating={self.average_rating}'

    def toJSON(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'profiles-rated': self.profiles_rated,
            'tier-points': self.points,
            'tier': self.tier,
            'times-rated': self.times_rated,
            'total-rating': self.total_rating,
            'average-rating': self.average_rating,
            'remaining-views': self.remaining_views
        }

    def set_password(self, password):
        # Create hashed password
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        # Check hashed password
        return check_password_hash(self.password, password)

    def rate_profile(self):
        # Temporary method logic, change as needed
        self.points += 1

        if self.points < 5:
            self.tier = self.points
            self.remaining_views = self.tier * 10

    def recieve_rating(self, rating):
        # Add a rating to the user's profile
        self.times_rated += 1
        self.total_rating += rating
        self.average_rating = self.total_rating / self.times_rated
