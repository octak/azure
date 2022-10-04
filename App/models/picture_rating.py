from App.database import db

picture_ratings = db.Table('picture_ratings',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('picture_id', db.Integer, db.ForeignKey('picture.id'))
)