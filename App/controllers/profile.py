from App.models import *
from App.database import db

def create_profile():
    feed = Feed.query.first() 
    profile = Profile()
    profile.views_left = feed.tier_view_dict[str(1)]
    db.session.add(profile)
    db.session.commit()
    return profile

def get_all_profiles():
    return Profile.query.all()

def get_all_profiles_json():
    profiles = Profile.query.all()
    if not profiles:
        return []
    profiles = [profile.toJSON() for profile in profiles]
    return profiles

def add_picture_to_profile(profileID, pictureID):
    profile = Profile.query.filter_by(id=profileID).first()
    picture = Picture.query.filter_by(id=pictureID).first()
    profile.pictures.append(picture)
    db.session.commit()

def add_rating_to_profile(profileID, ratingID):
    rating = ProfileRating.query.filter_by(id=ratingID).first()
    rated_profile = Profile.query.filter_by(id=profileID).first()
    rater_profile = Profile.query.filter_by(id=rating.rater_profile_id).first()
    feed = Feed.query.first() 
    init_tier = rater_profile.tier
    rated_profile.ratings.append(rating)
    rated_profile.increase_rating(rating.value)
    rater_profile.increase_tier_points()
    rater_profile.update_tier()
    final_tier = rater_profile.tier
    if init_tier != final_tier:
        rater_profile.views_left = feed.tier_view_dict[str(final_tier)]
    db.session.commit()