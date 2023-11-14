
from flask import Flask
from flask_restful import Api

from controllers.userController import login, logout, getUser, getAllUser


def initialRoutes(api):

    # [POST] LOGIN
    api.add_resource(login,"/login/<string:account_id>",endpoint="user_login")

    # [GET] LOGOUT
    api.add_resource(logout,"/logout",endpoint="user_logout")

    # [GET] GET USER
    api.add_resource(getUser,"/user_info/<string:account_id>", endpoint="get_user")

    # [GET] GET ALL USERS
    api.add_resource(getAllUser,"/all_user_info", endpoint="get_all_user")