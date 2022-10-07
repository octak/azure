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

# def get_all_users_json():
#     users = User.query.all()
#     if not users:
#         return []
#     users = [user.toJSON() for user in users]
#     return users

def create_user(username, password):
    newuser = User(username=username, password=password)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def link_user_profile(userID, profileID):
    user = User.query.get(userID)
    profile = Profile.query.get(profileID)

    if not user or not profile:
        return False

    user.profile = profile
    db.session.commit()

    return True

def get_all_users():
    return User.query.all()

def get_all_users_json():
    users = User.query.all()
    return [user.toJSON() for user in users] if users else [] 

def get_user_by_id(userID):
    return User.query.get(userID)

def get_user_by_username(username):
    return User.query.filter_by(username=username).first()

def update_username(userID, username):
    user = get_user_by_id(userID)

    if not user:
        return False

    user.username = username
    db.session.add(user)
    db.session.commit()
    
    return True


