from platform import architecture
from App.controllers import profile as profile_controller, feed as feed_controller
from flask import Blueprint, Flask, jsonify, make_response, redirect, render_template, request, send_from_directory
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

from App.controllers.auth import identity

profile_views = Blueprint("profile_views", __name__, template_folder="../templates")

def profile_from_identity(identity):
    if identity:
        profile = profile_controller.get_profile(identity)
        if profile:
            return profile
    return None

@profile_views.route("/profile", methods=["POST"])
def create_new_profile():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']

    if profile_controller.create_profile(username, password):
        return {'message': 'PROFILE CREATED'}, 201
    else:
        return {'message': 'USERNAME ALREADY TAKEN'}, 400


@profile_views.route("/profiles", methods=["GET"])
def get_all_profiles():
    profiles = profile_controller.get_all_profiles()
    return profile_controller.serialize_profiles(profiles)


@profile_views.route("/profile", methods=["GET"])
@jwt_required()
def get_active_profile():
    profile = profile_from_identity(get_jwt_identity())
    if profile:
        return profile.serialize()
    else:
        return {'message' : 'INVALID CREDENTIALS'}, 401


@profile_views.route("/profiles/<id>", methods=["GET"])
def get_profile(id):
    profile = profile_controller.get_profile(int(id))
    return profile.serialize() if profile else {'message': 'NON-EXISTENT PROFILE'}


@profile_views.route('/login', methods=['GET'])
def login():
    request_data = request.get_json()
    username = request_data['username']
    password = request_data['password']

    if username and password:
        profile = profile_controller.get_profile(username)
        if profile and profile.check_password(password):
            token =  create_access_token(identity=username)
            return jsonify(token=token)
    else:
        return jsonify({'message' : 'INVALID CREDENTIALS'}), 401


@profile_views.route('/profiles/rating', methods=['POST'])
@jwt_required()
def add_profile_rating():
    request_data = request.get_json()
    ratee_id = request_data['ratee_id']
    value = request_data['value']
     
    active_profile = profile_from_identity(get_jwt_identity())
    if not active_profile:
        return jsonify({'message' : 'INVALID CREDENTIALS'}), 401
    
    if not profile_controller.get_profile(ratee_id):
        return jsonify({'message' : 'NON-EXISTENT PROFILE'}), 401

    profile_controller.rate_profile(active_profile.id, ratee_id, value)

    return jsonify({'message' : 'SUCCESS'}), 201


@profile_views.route('/pictures/rating', methods=['POST'])
@jwt_required()
def add_picture_rating():
    request_data = request.get_json()
    ratee_id = request_data['ratee_id']
    value = request_data['value']

    active_profile = profile_from_identity(get_jwt_identity())
    if not active_profile:
        return jsonify({'message' : 'INVALID CREDENTIALS'}), 401
    
    if not profile_controller.get_picture(int(ratee_id)):
        return jsonify({'message' : 'NON-EXISTENT PICTURE'}), 401

    profile_controller.rate_picture(active_profile.id, ratee_id, value)

    return jsonify({'message' : 'SUCCESS'}), 201


@profile_views.route("/picture", methods=["POST"])
@jwt_required()
def upload_picture():
    request_data = request.get_json()
    url = request_data['url']

    active_profile = profile_from_identity(get_jwt_identity())

    if not active_profile:
        return jsonify({'message' : 'INVALID CREDENTIALS'}), 401

    if not url:
        return jsonify({'message' : 'INVALID URL'}), 401

    profile_controller.upload_picture(active_profile.id, url)
    
    return jsonify({'message' : 'SUCCESS'}), 201    


@profile_views.route("/pictures", methods=["GET"])
@jwt_required()
def get_active_profile_pictures():
    active_profile = profile_from_identity(get_jwt_identity())

    if not active_profile:
        return {'message' : 'INVALID CREDENTIALS'}, 401

    return active_profile.serialize_pictures()


@profile_views.route("/profiles/<id>/pictures", methods=["GET"])
def get_pictures_from_profile(id):
    profile = profile_controller.get_profile(int(id))
    if profile:
        return profile.serialize_pictures()
    else:
        return {'message': 'NON-EXISTENT PROFILE'}


@profile_views.route("/feed", methods=["GET"])
@jwt_required()
def get_feed():
    active_profile = profile_from_identity(get_jwt_identity())

    if not active_profile:
        return {'message' : 'INVALID CREDENTIALS'}, 401

    feed = feed_controller.generate_feed()
    if feed != []:
        return profile_controller.serialize_profiles(feed)
    else:
        return {'message': 'NO VIEWABLE PROFILES REMAINING, CHECK BACK IN 25 HOURS'}
