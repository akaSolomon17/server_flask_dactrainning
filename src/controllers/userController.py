import json, jwt, os

from datetime import datetime, timedelta

from dotenv import load_dotenv

from flask import Flask, request, make_response
from flask_restful import Resource, Api

from configs.errorStatus import errorStatus

load_dotenv()
errConfig = errorStatus()

REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")

app = Flask(__name__)
api = Api(app)

def createRefreshToken(payload):
    exp_time = datetime.now() + timedelta(days = 7)
    return jwt.encode({"some": payload,"exp":exp_time},REFRESH_TOKEN_SECRET,algorithm="HS256")

# DATA
accounts = {
    "ngohuy":{
        "first_name":"tran ngo",
        "last_name":"quoc huy",
        "email":"ngohuydn123",
        "password":"1234"
    },
    "ngohuy123":{
        "first_name":"tran ngopo",
        "last_name":"quoc huy",
        "email":"ngohuydn123",
        "password":"1234"
    }
}


    # LOGIN
class login(Resource):
    def post(self, account_id):
        try:
            content_type = request.headers.get('Content-Type')
            if content_type == "application/json":
                json= request.get_json()
                email = json["email"]
                password = json["password"]

                if not accounts.get(account_id):
                    return errConfig.statusCode("This account id not exist!",401)

                if password=="" or email=="":
                    return errConfig.statusCode("Please fill in email/password field!",401)
            
                if accounts[account_id]["email"] != email :
                    return errConfig.statusCode("Wrong email!",401)

                if accounts[account_id]["password"] != password :
                    return errConfig.statusCode("Wrong password!",401)
                
                
                refresh_token = createRefreshToken(account_id)
                response = make_response().set_cookie('RefreshToken', 
                                            refresh_token, 
                                            max_age=7 * 24 * 60 * 60 * 1000, 
                                            httponly=True, 
                                            path='/refresh_token')

                return response

            else: return "Content-Type not support!"
        except KeyError:
            return errConfig.statusDefault(4)


    # GET USER INFOR
class getUser(Resource):
    def get(self,account_id):
        return {account_id: accounts[account_id]}


    # GET ALL USER INFO
class getAllUser(Resource):
    
    def get(self):
        return accounts


    # LOGOUT
class logout(Resource):
    def get(self):
        return errConfig.statusCode("Logout successful!")
