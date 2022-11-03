from App.extensions import db


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("profile.id"))
    url = db.Column(db.String, nullable=False)
