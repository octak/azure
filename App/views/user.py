from App.controllers import *
from flask import Blueprint, jsonify, render_template, request, send_from_directory
from flask_jwt import jwt_required
import json

user_views = Blueprint('user_views', __name__, template_folder='../templates')

# @user_views.route('/users', methods=['GET'])
# def get_user_page():
#     users = get_all_users()
#     return render_template('users.html', users=users)

# @user_views.route('/static/users')
# def static_user_page():
#   return send_from_directory('static', 'static-user.html')

@user_views.route('/api/users')
@jwt_required()
def client_app():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/<username>/pictures')
def view_profile_pictures(username):
    pictures = get_all_pictures_from_profile(username)
    return jsonify(pictures)

@user_views.route('/api/<username>/rated-profiles')
def view_rated_profiles(username):
    profiles = get_rated_profiles(username)
    return jsonify(profiles)

@user_views.route('/api/<username>/rated-pictures')
def view_rated_pictures(username):
    pictures = get_rated_pictures(username)
    return jsonify(pictures)

@user_views.route('/api/<username>/rated-by')
def view_profile_raters(username):
    profiles = get_profile_raters(username)
    return jsonify(profiles)