from App.database import db
from App.models import *
from App.controllers import *

# def add_rating_to_profile(profileID, ratingID):
#     rating = ProfileRating.query.filter_by(id=ratingID).first()
#     rated_profile = Profile.query.filter_by(id=profileID).first()
#     rater_profile = Profile.query.filter_by(id=rating.rater_profile_id).first()
#     feed = get_feed()
#     init_tier = rater_profile.tier
#     rated_profile.ratings.append(rating)
#     rated_profile.increase_rating(rating.value)
#     rater_profile.increase_tier_points()
#     rater_profile.update_tier()
#     final_tier = rater_profile.tier
#     if init_tier != final_tier:
#         rater_profile.views_left = feed.tier_view_dict[str(final_tier)]
#     db.session.commit()

# def get_all_profiles_json():
#     profiles = Profile.query.all()
#     if not profiles:
#         return []
#     profiles = [profile.toJSON() for profile in profiles]
#     return profiles

# def add_picture_to_profile(profileID, pictureID):
#     profile = Profile.query.filter_by(id=profileID).first()
#     picture = Picture.query.filter_by(id=pictureID).first()
#     profile.pictures.append(picture)
#     db.session.commit()

# def rate_profile(rater_id, rated_id, rating_value):
#     rater_profile = Profile.query.filter_by(id=rater_id).first()
#     rated_profile = Profile.query.filter_by(id=rated_id).first()
#     if not rater_profile or not rated_profile:
#         return False
#     rating = ProfileRating.query.filter_by(rater_profile_id=rater_id, rated_profile_id=rated_id).first()
#     if rating:
#         rated_profile.update_rating(rating.value - rating_value)
#         rating.value = rating_value
#     else:
#         rating = ProfileRating(rated_profile_id=rated_id, rater_profile_id=rater_id, value=rating_value)
#         rated_profile.receive_rating(rating_value)
#         old_tier = rater_profile.tier
#         rater_profile.increase_tier_points()
#         new_tier = rater_profile.tier
#         feed = Feed.query.first()
#         if old_tier != new_tier:
#             rater_profile.views_left = feed.tier_view_dict[str(new_tier)]
#     db.session.add(rated_profile)
#     db.session.add(rating)
#     db.session.commit()
#     return True

# def rate_picture(rater_id, rated_id, rating_value):
#     rater_profile = Profile.query.filter_by(id=rater_id).first()
#     rated_picture = Picture.query.filter_by(id=rated_id).first()
#     if not rater_profile or not rated_picture:
#         return False
#     rating = PictureRating.query.filter_by(rater_profile_id=rater_id, rated_picture_id=rated_id).first()
#     if rating:
#         rated_picture.update_rating(rating.value - rating_value)
#         rating.value = rating_value
#     else:
#         rating = PictureRating(rated_picture_id=rated_id, rater_profile_id=rater_id, value=rating_value)
#         rated_picture.receive_rating(rating_value)
#     db.session.add(rated_picture)
#     db.session.add(rating)
#     db.session.commit()
#     return True

def create_profile():
    feed = Feed.query.first()
    profile = Profile()
    profile.views_left = feed.tier_view_dict[str(1)]
    db.session.add(profile)
    db.session.commit()
    return profile

def get_all_profiles_json():
    profiles = Profile.query.all()
    return [profile.toJSON() for profile in profiles] if profiles else []

def get_profile_by_id(profileID):
    return Profile.query.get(profileID)

def add_picture_to_profile(profileID, image_url):
    profile_ = Profile.query.get(profileID)
    if not profile_:
        return False
    picture = Picture(url=image_url, profile=profile_)
    db.session.add(picture)
    db.session.commit()
    return True

def get_all_pictures_from_profile(profileID):
    pictures = Profile.query.get(profileID).pictures
    return pictures if pictures else []

def rate_profile(rater_id, ratee_id, value_):
    rater_ = Profile.query.get(rater_id)
    ratee_ = Profile.query.get(ratee_id)
    if not rater_ or not ratee_:
        return False
    rating = ProfileRating.query.get((rater_id, ratee_id))    
    if rating:
        ratee_.update_rating(rating.value - value_)
        rating.value = value_
    else:
        rating = ProfileRating(rater=rater_, ratee=ratee_, value=value_)
        ratee_.receive_rating(value_)
        old_tier = rater_.tier
        rater_.increase_tier_points()
        new_tier = rater_.tier
        feed = Feed.query.first()
        if old_tier != new_tier:
            rater_.views_left = feed.tier_view_dict[str(new_tier)]
    db.session.add([rater_, ratee_, rating])
    db.session.commit()
    return True

def rate_picture(rater_id, ratee_id, value_):
    rater_ = Profile.query.get(rater_id)
    ratee_ = Picture.query.get(ratee_id)
    if not rater_ or not ratee_:
        return False
    rating = PictureRating.query.get((rater_id, ratee_id))
    if rating:
        ratee_.update_rating(rating.value - value_)
        rating.value = value_
    else:
        rating = PictureRating(rater=rater_, ratee=ratee_, value=value_)
        ratee_.receive_rating(value_)
    db.session.add([rater_, ratee_, rating])
    db.session.commit()
    return True