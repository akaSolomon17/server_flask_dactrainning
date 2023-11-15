import json, jwt, os

from jwt.exceptions import InvalidTokenError, DecodeError, ExpiredSignatureError, InvalidSignatureError
from datetime import datetime, timedelta

from dotenv import load_dotenv

from flask import Flask, request, make_response
from flask_restful import Resource, Api

from configs.errorStatus import errorStatus

app = Flask(__name__)
api = Api(app)

# Load variables in .env environment
load_dotenv()
# Status code config to JSON
errConfig = errorStatus()

REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

def createRefreshToken(payload):
    exp_time = datetime.now() + timedelta(days = 7)
    
    payload = {
        "payload": payload,
        "exp": exp_time
    }
    
    return jwt.encode(payload,REFRESH_TOKEN_SECRET,algorithm="HS256")

def createAccessToken(payload):
    exp_time = datetime.now() + timedelta(minutes=15)
    
    payload = {
        "payload": payload,
        "exp": exp_time
    }
    
    return jwt.encode(payload,ACCESS_TOKEN_SECRET,algorithm="HS256")

# DATA
accounts = {
    "1a":{
        "first_name":"tran ngo",
        "last_name":"quoc huy",
        "email":"ngohuydn123",
        "password":"1234",
        "createAt":"",
        "updateAt":""
    },
    "2a":{
        "first_name":"tran",
        "last_name":"huy",
        "email":"ngohuydn123",
        "password":"ngohuy123",
        "createAt":"",
        "updateAt":""
    },
    "3a":{
        "first_name":"solo",
        "last_name":"mon",
        "email":"ngohuydn123",
        "password":"solomon1",
        "createAt":"",
        "updateAt":""
    },
    "4a":{
        "first_name":"than thi",
        "last_name":"thao",
        "email":"thanthithao111",
        "password":"thanthao1",
        "createAt":"",
        "updateAt":""
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
                response = errConfig.statusCode("Login successful!")
                # response.set_cookie('RefreshToken', refresh_token,max_age=604800000,httponly=True,path='/refresh_token')
                response.set_cookie('RefreshToken', refresh_token, 604800000, None, '/refresh_token', None, None, True)
                return response

            else: return "Content-Type not support!"
        except Exception as e :
            return errConfig.statusCode(str(e),500)
    # Get ACCESS_TOKEN
class getAccessToken(Resource):
    def post(self):
        try:
            json = request.get_json()
            account_id = json["account_id"]

            refresh_token = request.cookies.get('RefreshToken')
            if not refresh_token:
                return errConfig.statusCode("Please login again!",401)

            try:
                jwt.decode(refresh_token,REFRESH_TOKEN_SECRET,"HS256")

                access_token = createAccessToken(account_id)

                return errConfig.msgFeedback(access_token)

            except InvalidTokenError:
                return errConfig.statusCode("Invalid token",401)
            except DecodeError:
                return errConfig.statusCode("Token failed validation",401)
            except InvalidSignatureError:
                return errConfig.statusCode("Invalid refresh token",401)
            except ExpiredSignatureError:
                return errConfig.statusCode("The RF token is expired",401)
            except Exception as e:
                return errConfig.statusCode(f"An unexpected error occurred:{str(e)}",500)
        except Exception as e:
            return str(e)

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
        try:
            response = errConfig.statusCode("Logout successful!")
            response.delete_cookie('RefreshToken','/refresh_token')
            return response
        except:
            pass
