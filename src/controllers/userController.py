import json, jwt, os,re
import bcrypt

from jwt.exceptions import *
from datetime import datetime, timedelta

from dotenv import load_dotenv
#FLASK
from flask import Flask, request, make_response,jsonify
from flask_restful import Resource, Api


from auth.auth import authMiddleware
from auth.authAdmin import authMiddlewareAdmin

from configs.errorStatus import errorStatus

app = Flask(__name__)
api = Api(app)

# Load variables in .env environment
load_dotenv()
# Status code config to JSON
errConfig = errorStatus()

REFRESH_TOKEN_SECRET = os.getenv("REFRESH_TOKEN_SECRET")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")

# Create Refresh Token
def createRefreshToken(payload):
    exp_time = datetime.now() + timedelta(days = 7)
    
    payload = {
        "payload": payload,
        "exp": exp_time
    }
    
    return jwt.encode(payload,REFRESH_TOKEN_SECRET,algorithm="HS256")
# Create Access Token
def createAccessToken(payload):
    exp_time = datetime.now() + timedelta(minutes=15)
    
    payload = {
        "payload": payload,
        "exp": exp_time
    }
    
    return jwt.encode(payload,ACCESS_TOKEN_SECRET,algorithm="HS256")

def validate_email(email):
    pattern = re.compile(r'^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$')
    # Kiểm tra địa chỉ email
    return pattern.match(email) is not None

def find_user_by_email(email):
    from initSQL import db
            
    from models.userModel import User
    user = User.query.filter_by(email=email).first()
    return user
# USER MODELS
    # LOGIN
class login(Resource):
    def post(self):
        
        try:
            content_type = request.headers.get('Content-Type')
            if content_type == "application/json":
                json= request.get_json()
                email = json["email"]
                password = json["password"]
                user_id = json["user_id"]
                if password=="" or email=="":
                    return errConfig.statusCode("Please fill in email/password field!",401)
                
                User = User.query.filter_by(user_id = user_id).one_or_404('Account is not exist!')

                if User.password != password :
                    return errConfig.statusCode("Wrong password!",401)
                 
                refresh_token = createRefreshToken(User.user_id)
                
                response = errConfig.statusCode("Login successful!")
                response.set_cookie('RefreshToken', refresh_token, max_age=7*24*60*60*1000, path='/api/refresh_token', httponly=True)
                
                return response

            else: return "Content-Type not support!"
            
        except Exception as e :
            return errConfig.statusCode(str(e),500)
    
    # Get ACCESS_TOKEN
class getAccessToken(Resource):
    def post(self):
        from initSQL import db
                
        from models.userModel import User
        try:
            json= request.get_json()
            user_id = json["user_id"]
            
            User = User.query.filter_by(user_id = user_id).one_or_404()
            
            refresh_token = request.cookies.get('RefreshToken')
            if not refresh_token:
                return errConfig.statusCode("Please login again!",401)

            try:
                jwt.decode(refresh_token,REFRESH_TOKEN_SECRET,"HS256")

                access_token = createAccessToken(User.user_id)

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
    @authMiddleware
    def get(self,user_id):
        from initSQL import db
        from models.userModel import User
        
        User = User.query.filter_by(user_id = user_id).one_or_404()
        User_dict = User.__dict__
        User_dict.pop('_sa_instance_state', None) # Disable _sa_instance_state of SQLAlchemy (_sa_instance_state can't convert JSON)
        
        return jsonify(User_dict)

    # GET ALL USER INFO
class getAllUser(Resource):
    from initSQL import db
    from models.userModel import User
    
    def get(self):
        Users = db.session.execute(db.select(User).order_by(User.user_id)).scalar()
        # Users = db.query(db.select(User).order_by(User.user_id))
        Users_dict = Users.__dict__
        Users_dict.pop('_sa_instance_state', None)
        return Users_dict


    # LOGOUT
class logout(Resource):
    def get(self):
        try:
            response = errConfig.statusCode("Logout successful!")
            response.delete_cookie('RefreshToken','/api/refresh_token')
            return response
        except Exception as e:
            return errConfig.statusDefault(4)

    # DELETE USER
class deleteUser(Resource):
    @authMiddleware
    @authMiddlewareAdmin
    def delete(self):
        from initSQL import db
        from models.userModel import User
        try:
            json = request.get_json()
            user_id = json['user_id']
            
            User = User.query.filter_by(user_id = user_id).one_or_404()
            if User:
                db.session.delete(User)
                db.session.commit()
                return errConfig.statusCode("Delete User successfully!")
            else:
                return 
            
        except Exception as e:
            # return errConfig.statusDefault(4)
            return errConfig.statusCode(str(e),500)
    
    # ADD USER    
class addUser(Resource):
    @authMiddlewareAdmin
    def post(self):
        from initSQL import db
        from models.userModel import User

        try:
            json = request.get_json()
            first_name = json['first_name']
            last_name = json['last_name']
            email = json['email']
            password = json['password'].encode('utf-8')
            role_id = json['role_id']
            
            if not validate_email:
                return errConfig.statusCode("Invalid email",400)
            
            if find_user_by_email(email):
                return errConfig.statusCode("Email already in exist",400)
                                            
            if len(password) < 6:
                return errConfig.statusCode("Password must be at least 6 characters.",400)
            
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            
            User(first_name,last_name,email,password,role_id)
            db.session.add(User)
            db.session.commit()
            return errConfig.statusCode("Add User successfully!")
        except Exception as e:
            return errConfig.statusCode(str(e),500)