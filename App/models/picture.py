from App.database import db


class Picture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    url = db.Column(db.String, nullable=False)
