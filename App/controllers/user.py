from App.database import db
import json
from App.models import Picture, User, Profile

# def create_user(username, password):
#     temp_user = get_user_by_username(username)

#     if not temp_user:
#         newuser = User(username=username, password=password)
#         db.session.add(newuser)
#         db.session.commit()
#         return newuser
#     return None

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def add_profile_to_user(userID, profileID):
    user = User.query.filter_by(id=userID).first()
    profile = Profile.query.filter_by(id=profileID).first()
    user.profile = profile
    db.session.commit()

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    if not users:
        return []
    users = [user.toJSON() for user in users]
    return users

def get_user(id):
    return User.query.get(id)

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def update_username(id, username):
    user = get_user(id)
    if user:
        user.username = username
        db.session.add(user)
        return db.session.commit()
    return None

def upload_image(id, url_arg):
    user = get_user(id)
    if user:
        picture = Picture(url=url_arg, uploader=user)
        db.session.add(picture)
        return db.session.commit()
    return None

def get_picture(id):
    return Picture.query.get(id)

def get_all_pictures():
    return Picture.query.all()
