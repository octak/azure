from App.database import db
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    profiles_rated = db.Column(db.Integer, nullable=False, default=0)
    points = db.Column(db.Integer, nullable=False, default=0)
    tier = db.Column(db.Integer, nullable=False, default=1)

    times_rated = db.Column(db.Integer, nullable=False, default=0)
    total_rating = db.Column(db.Integer, nullable=False, default=0)
    average_rating = db.Column(db.Integer, nullable=False, default=0)

    # Profile visibility information could possibly be stored in another database
    remaining_views = db.Column(db.Integer, nullable=False, default=0)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def toJSON(self):
        return{
            'id': self.id,
            'username': self.username
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def update_tier(self):
       self.points += 1

       match self.points:
        case 10:
            self.tier = 10
        