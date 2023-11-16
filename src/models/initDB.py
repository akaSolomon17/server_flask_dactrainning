import os

from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# Load variables in .env environment
load_dotenv()
DB_URL = os.getenv('DB_URL')

app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()

db.create_all()