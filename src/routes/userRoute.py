
from flask import Flask
from flask_restful import Api

from controllers.userController import login, logout, getUser, getAllUser, getAccessToken


def initialRoutes(api):

    # [POST] LOGIN
    api.add_resource(login,"/api/login/<string:account_id>", endpoint="user_login")

    # [POST] LOGIN
    api.add_resource(getAccessToken,"/api/refresh_token", endpoint="refresh_token")

    # [GET] LOGOUT
    api.add_resource(logout,"/api/logout", endpoint="user_logout")

    # [GET] GET USER
    api.add_resource(getUser,"/api/user_info/<string:account_id>", endpoint="get_user")

    # [GET] GET ALL USERS
    api.add_resource(getAllUser,"/api/all_user_info", endpoint="get_all_user")