from flask import Blueprint, jsonify

from ..service.user_service import UserService
helloworld_bp= Blueprint('helloworld', __name__)

user_service= UserService()
@helloworld_bp.route('/user')
def user():

    #print("Printing in console")
    return "welcome to your first controller "+user_service.get_user().name + " !!"


@helloworld_bp.route('/users')
def users():
    users = user_service.get_all_users()
    users_dict = [user.__dict__ for user in users]  # Convert objects to dicts
    return jsonify(users_dict)