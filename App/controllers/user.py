import json
from App.database import db
from App.models import Picture, Profile, User

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def new_profile(user_):
    if not user_.profile:
        user_.profile = Profile()
        db.session.add(user_)
        db.session.commit()
    return user_.profile
    
# def add_profile_to_user(userID, profileID):
#     user = User.query.get(userID)
#     profile = Profile.query.get(profileID)
#     if not user or not profile:
#         return False
#     user.profile = profile
#     db.session.commit()
#     return True

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    return [user.toJSON() for user in users] if users else [] 

def get_user_by_id(userID):
    return User.query.get(userID)

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

# def update_username(userID, username):
#     user = User.query.get(userID)
#     if not user:
#         return False
#     user.username = username
#     db.session.add(user)
#     db.session.commit()
#     return True

def update_username(user, username):
    user.username = username
    db.session.add(user)
    db.session.commit()