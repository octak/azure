from App.controllers import profile as profile_controller
from flask import (Blueprint, jsonify, redirect, render_template, request, send_from_directory)
from flask_jwt import jwt_required

profile_views = Blueprint("profile_views", __name__, template_folder="../templates")


@profile_views.route("/api/profiles", methods=["GET"])
def get_all_profiles():
    profiles = profile_controller.get_all_profiles()
    return jsonify([profile.toJSON() for profile in profiles])


@profile_views.route("/api/profiles/<id>", methods=["GET"])
def get_profile(id):
    profile = profile_controller.get_profile(id)
    return jsonify(profile.toJSON()) if profile else jsonify({'message': 'Profile does not exist.'})


@profile_views.route("/api/profiles/<id>/uploads", methods=["GET"])
def get_pictures_from(id):
    profile = profile_controller.get_profile(id)
    return (
        jsonify([picture.toJSON() for picture in profile.pictures])
        if profile
        else jsonify({'message': 'Profile does not exist.'})
    )


@profile_views.route("/profile", methods=["POST"])
def create_new_profile():
    """
    Request body:
        {
            "username" : username
            "password" : password
        }
    """
    profile_data = request.get_json()
    if profile_controller.create_profile(
        profile_data["username"], profile_data["password"]
    ):
        return jsonify({"message", "Profile created."})
    return jsonify({"message", "Profile with that username already exists."})


@profile_views.route("/picture", methods=["POST"])
def upload_picture(username):
    """
    Request body:
        {
            "username" : username
            "url" : url
        }
    """
    profile = profile_controller.get_profile(username)
    if not profile:
        return jsonify({"message", "Failure"})
    picture_data = request.get_json()
    profile_controller.upload_picture(username, picture_data["url"])
    return jsonify({"message", "Picture sucessfully uploaded."})


@profile_views.route("/pictures/rating", methods=["POST"])
def rate_profile(username):
    """
    Request body:
        {
            "rater_id" : username
            "ratee_id" : username
            "value" : url
        }
    """
    profile = get_profile(username)
    if not profile:
        return jsonify({"message", "Failure"})
    rating_data = request.get_json()
    # REMEMBER TO ENSURE THAT THE RATED PROFILE ACTUALLY EXISTS
    profile_controller.rate_profile(
        rating_data["rater_id"], rating_data["ratee_id"], rating_data["value"]
    )
    return jsonify({"message", "Success"})


@profile_views.route("/profiles/rating", methods=["POST"])
def rate_picture(username):
    """
    Request body:
        {
            "rater_id" : username
            "ratee_id" : picture_id
            "value" : url
        }
    """
    profile = get_profile(username)
    if not profile:
        return jsonify({"message", "Failure"})
    rating_data = request.get_json()
    # REMEMBER TO ENSURE THAT THE RATED PICTURE ACTUALLY EXISTS
    profile_controller.rate_profile(
        rating_data["rater_id"], rating_data["ratee_id"], rating_data["value"]
    )
    return jsonify({"message", "Success"})
