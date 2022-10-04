from App.database import db

class Picture(db.Model):
    # Fields
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String, nullable=False)

    times_rated = db.Column(db.Integer, nullable=False, default=0)
    total_rating = db.Column(db.Integer, nullable=False, default=0)
    average_rating = db.Column(db.Integer, nullable=False, default=0)

    # Relationship Stuff
    uploader_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
