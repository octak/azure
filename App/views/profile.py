from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from App import create_profile, get_profile, get_profiles, to_dict_users, to_dict_user, rate_profile, get_picture, \
    rate_picture, create_picture, to_dict_pictures, generate_feed

profile_views = Blueprint("profile_views", __name__, template_folder="../templates")


def profile_from_identity(identity):
    return get_profile(identity) if identity else None


@profile_views.route("/profile", methods=["POST"])
def create_new_profile():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']

    if create_profile(username, password):
        return {'message': 'created'}, 201
    else:
        return {'message': 'username unavailable'}, 400


@profile_views.route("/profiles", methods=["GET"])
def get_all_profiles():
    return to_dict_users(get_profiles())


@profile_views.route("/profile", methods=["GET"])
@jwt_required()
def get_active_profile():
    profile = profile_from_identity(get_jwt_identity())
    if profile:
        return to_dict_user(profile)
    else:
        return {'message': 'invalid credentials'}, 401


@profile_views.route("/profiles/<int:profile_id>", methods=["GET"])
def route_get_profile(profile_id):
    profile = get_profile(profile_id)
    return to_dict_user(profile) if profile else ({'message': 'profile does not exist'}, 404)


@profile_views.route('/login', methods=['POST'])
def login():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']

    if username and password:
        profile = get_profile(username)
        if profile and profile.check_password(password):
            token = create_access_token(identity=username)
            return jsonify(token=token), 201
    else:
        return jsonify({'message': 'INVALID CREDENTIALS'}), 401


@profile_views.route('/profiles/rating', methods=['POST'])
@jwt_required()
def add_profile_rating():
    request_data = request.get_json()
    ratee_id = request_data['ratee_id']
    value = request_data['value']

    active_profile = profile_from_identity(get_jwt_identity())
    if not active_profile:
        return jsonify({'message': 'invalid credentials'}), 401

    if not get_profile(ratee_id):
        return jsonify({'message': 'profile does not exist'}), 401

    rate_profile(active_profile.id, ratee_id, value)

    return jsonify({'message': 'successful'}), 201


@profile_views.route('/pictures/rating', methods=['POST'])
@jwt_required()
def add_picture_rating():
    request_data = request.get_json()
    ratee_id = request_data['ratee_id']
    value = request_data['value']

    active_profile = profile_from_identity(get_jwt_identity())
    if not active_profile:
        return jsonify({'message': 'invalid credentials'}), 401

    if not get_picture(int(ratee_id)):
        return jsonify({'message': 'picture does not exist'}), 401

    rate_picture(active_profile.id, ratee_id, value)

    return jsonify({'message': 'successful'}), 201


@profile_views.route("/picture", methods=["POST"])
@jwt_required()
def upload_picture():
    request_data = request.get_json()
    url = request_data['url']

    active_profile = profile_from_identity(get_jwt_identity())

    if not active_profile:
        return jsonify({'message': 'invalid credentials'}), 401

    if not url:
        return jsonify({'message': 'invalid url'}), 401

    create_picture(active_profile.id, url)

    return jsonify({'message': 'successful'}), 201


@profile_views.route("/pictures", methods=["GET"])
@jwt_required()
def get_active_profile_pictures():
    active_profile = profile_from_identity(get_jwt_identity())

    if not active_profile:
        return {'message': 'invalid credentials'}, 401

    return to_dict_pictures(active_profile.pictures), 200


@profile_views.route("/profiles/<int:profile_id>/pictures", methods=["GET"])
def get_pictures_from_profile(profile_id):
    profile = get_profile(profile_id)
    if profile:
        return to_dict_pictures(profile.pictures)
    else:
        return {'message': 'profile does not exist'}, 404


@profile_views.route("/feed", methods=["GET"])
@jwt_required()
def get_feed():
    active_profile = profile_from_identity(get_jwt_identity())

    if not active_profile:
        return {'message': 'invalid credentials'}, 401

    feed_listing = generate_feed()
    if feed_listing:
        return to_dict_users(feed_listing)
    else:
        return {'message': 'no viewable profiles, check again tomorrow'}, 404
