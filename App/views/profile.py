from flask import Blueprint, request
from flask_jwt_extended import create_access_token, jwt_required, current_user

from App.controllers import *
from App.extensions import jwt

profile_views = Blueprint("profile_views", __name__, template_folder="../templates")


@jwt.user_identity_loader
def user_identity_lookup(user: Profile):
    return user.id


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return get_profile(identity)


@profile_views.route("/profiles", methods=["GET"])
def all_profiles():
    """Returns all users."""
    return to_dict_profiles(get_profiles())


@profile_views.route("/profiles/<int:profile_id>", methods=["GET"])
def one_profile(profile_id):
    """Returns the user corresponding to provided ID."""
    user = get_profile(profile_id)
    if user:
        return to_dict_profile(user)
    else:
        return {'message': 'Profile does not exist.'}, 404


@profile_views.route("/profile", methods=["POST"])
def new_user():
    """Creates a user."""
    data = request.get_json()
    username = data['username']
    password = data['password']

    if create_profile(username, password):
        return {"message": "User created successfully."}, 200
    else:
        return {"message": "Username unavailable."}, 400


@profile_views.route("/profiles/<int:user_id>/pictures", methods=["GET"])
def user_posts(user_id):
    """Returns all a user's pictures."""
    user = get_profile(user_id)
    if user:
        return to_dict_pictures(user.pictures)
    else:
        return {'message': 'Profile does not exist.'}, 404


@profile_views.route("/login", methods=["POST"])
def login():
    """Authenticates a user and returns a JWT."""
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = get_profile(username)
    if user and user.check_password(password):
        token = create_access_token(identity=user)
        return {"token": token}, 200
    else:
        return {'message': 'Invalid credentials.'}, 401


@profile_views.route("/profile", methods=["GET"])
@jwt_required()
def current_user_():
    """Returns the profile that is currently logged-in."""
    if current_user:
        return to_dict_profile(current_user)
    else:
        return {'message': 'Invalid credentials.'}, 401


@profile_views.route("/profile/pictures", methods=["GET"])
@jwt_required()
def current_user_posts():
    """Returns the posts of the profile that is currently logged-in."""
    if current_user:
        return to_dict_pictures(current_user.pictures)
    else:
        return {'message': 'Invalid credentials.'}, 401


@profile_views.route("/picture", methods=["POST"])
@jwt_required()
def new_current_user_post():
    """Adds a post to the profile that is currently logged-in."""
    data = request.get_json()
    url = data['url']
    if current_user:
        create_picture(current_user.id, url)
        return {'message': 'Successful'}, 401
    else:
        return {'message': 'Invalid credentials.'}, 401


@profile_views.route("/profiles/rating", methods=["POST"])
@jwt_required()
def post_user_rating():
    """Adds or edits a rating for the selected user."""
    data = request.get_json()
    ratee_id = data['ratee_id']
    value = data['value']

    if not current_user:
        return {'message': 'Invalid credentials.'}, 401
    if not get_profile(ratee_id):
        return {'message': 'User does not exist.'}, 404

    rate_profile(current_user.id, ratee_id, value)

    return {'message': 'Successful.'}, 201


@profile_views.route("/pictures/rating", methods=["POST"])
@jwt_required()
def post_picture_rating():
    """Adds or edits a rating for the selected post."""
    data = request.get_json()
    ratee_id = data['ratee_id']
    value = data['value']

    if not current_user:
        return {'message': 'Invalid credentials.'}, 401
    if not get_picture(ratee_id):
        return {'message': 'Post does not exist.'}, 404

    rate_picture(current_user.id, ratee_id, value)

    return {'message': 'Successful.'}, 201


@profile_views.route("/feed", methods=["GET"])
@jwt_required()
def feed():
    if current_user:
        listing = generate_feed()
        if listing:
            return to_dict_profiles(listing)
        else:
            return {'message': 'No profiles can be viewed. Check again tomorrow.'}, 401
    else:
        return {'message': 'Invalid credentials.'}, 401
