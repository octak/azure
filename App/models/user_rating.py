from App.database import db

user_ratings = db.Table('user_ratings',
    db.Column('user_id_rater', db.Integer, db.ForeignKey('user.id')),
    db.Column('user_id_rated', db.Integer, db.ForeignKey('user.id'))
)