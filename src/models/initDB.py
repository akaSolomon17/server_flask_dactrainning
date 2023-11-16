# import os

# from flask import Flask
# from dotenv import load_dotenv
# from flask_sqlalchemy import SQLAlchemy

# # Load variables in .env environment
# load_dotenv()
# DB_URL = os.getenv('DB_URL')
# db = SQLAlchemy()
# def dbInit(app):
#     app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    

#     db.create_all()