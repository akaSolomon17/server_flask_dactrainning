import os, json

from flask import Flask, request, make_response
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

todos = {}
accounts = {
    "01":{
        "email": "quochuy1",
        "password": "huy1"
    }
}

class login(Resource):
    def get(self, account_id):
        return accounts

    def post(self, account_id):
        try:
            content_type = request.headers.get('Content-Type')

            if content_type == "application/json":
                json= request.get_json()

                email = json["email"]
                password = json["password"]

                if not password and email:
                    msg = "Please fill in the field password & email"
                    make_response({'message': msg}, 401)
                
                # Check email, mật khẩu ở trong accounts
                if account_id not in accounts:
                    make_response({'message':'Account is not exist'},400)
                
                if email not in account_id:
                    make_response({'message':'Wrong email, email not exist'},400) 

                if password not in account_id:
                    make_response({'message':'Wrong password!'},400) 
                
                return {'message': 'Login successful!'}
                # if account_id in accounts:
                #     if account_id[email] == email and account_id[password] == password:
                #         return f"{account_id}: Login success!"
                #     else: return f"{account_id}: Wrong email or password!"
                # else: return "There are no account in the system!"

            else: return "Content-Type not support!"
        except:
            make_response({'message':"HTTP error"},500)

class register(Resource):
    def post(self, account_id):
        try:
            json = request.get_json()

            first_name = json.get_json["first_name"]
            last_name = json.get_json["last_name"]
            email = json.get_json["first_name"]
            password = json.get_json["first_name"]

            # Check blank password & email
            if not password and email:
                msg = "Please fill in the field password & email"
                make_response({'message': msg}, 401)
            
            # Check exist email
        except:
            make_response({'message':"HTTP error"},500)
        
        
api.add_resource(login,"/login/<string:account_id>")
if __name__ == "__main__":
    app.run(debug=True)
