from flask_jwt import jwt_required
from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    send_from_directory,
)

from App.controllers import profile as profile_controller

profile_views = Blueprint("profile_views", __name__, template_folder="../templates")


@profile_views.route("/profiles", methods=["GET"])
def get_all_profiles():
    profiles = profile_controller.get_all_profiles()
    return jsonify([profile.toJSON() for profile in profiles])


@profile_views.route("/profiles/<username>", methods=["GET"])
def get_profile(username):
    profile = profile_controller.get_profile(username)
    return jsonify(profile.toJSON()) if profile else jsonify([])


@profile_views.route("/profiles/<username>/pictures", methods=["GET"])
def get_pictures_from(username):
    profile = profile_controller.get_profile(username)
    return (
        jsonify([picture.toJSON() for picture in profile.pictures])
        if profile
        else jsonify([])
    )


# Maybe API endpoint could be /profiles?rater=<username>
@profile_views.route("/profiles/<username>/rated-profiles", methods=["GET"])
def get_rated_profiles(username):
    profile = profile_controller.get_profile(username)
    return (
        jsonify([profile_.toJSON() for profile_ in profile.rated_profiles])
        if profile
        else jsonify([])
    )


# Maybe API endpoint could be /pictures?rater=<username>
@profile_views.route("/profiles/<username>/rated-pictures", methods=["GET"])
def get_rated_pictures(username):
    profile = get_profile(username)
    return (
        jsonify([picture.toJSON() for picture in profile.rated_pictures])
        if profile
        else jsonify([])
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
        return jsonify({"message", "Profile sucessfully created."})
    return jsonify({"message", "Error: Profile with that username already exists."})


@profile_views.route("/profiles/<username>/upload", methods=["POST"])
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


@profile_views.route("/profiles/<username>/rate-profile", methods=["POST"])
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


@profile_views.route("/profiles/<username>/rate-picture", methods=["POST"])
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
