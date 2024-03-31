from flask import Flask
from flask_sqlalchemy import SQLAlchemy # import the SQLAlchemy class from flask_sqlalchemy for ORM support
import os
from os import path # import path from os module to work with file paths
from dotenv import load_dotenv # import load_dotenv from dotenv to load .env files
from flask_login import LoginManager # import LoginManager from flask_login for handling user sessions

load_dotenv() # load environment variables

db = SQLAlchemy() # create an instance of SQLAlchemy for database operations
DB_NAME = os.getenv('DB_NAME') # retrieve the database name from environment variables
SECRET_KEY = os.getenv('SECRET_KEY') # retrieve the secret key from environment variables

def create_app():
    app = Flask(__name__) # instantiate a new Flask application
    app.secret_key = SECRET_KEY # set the secret key for the application
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # configure the database URI for SQLAlchemy
    db.init_app(app) # initialize the SQLAlchemy object with the Flask app for ORM support

    from .views import views # register the views blueprint with the application
    #from .auth import auth # register the views blueprint with the application

    app.register_blueprint(views, url_prefix="/")
    #app.register_blueprint(auth, url_prefix="/")

    from .models import Friendship, SharedStudySet, User, StudySet, QuestionAnswer, Audio

    with app.app_context():
        db.create_all() # create database tables for all models

    lm = LoginManager() # login manager creates a session, default = 30 days
    lm.login_view = "auth.login" # redirects to login page if user is not logged in
    lm.init_app(app) # initialize the LoginManager with the Flask app

    @lm.user_loader
    def load_user(id):
        user = User.query.filter_by(id=id) # query the database for a user with the given ID
        if user: # if a user is found, return the user object
            return user
    
    return app