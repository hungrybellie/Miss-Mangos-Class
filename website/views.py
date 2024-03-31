from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from .models import Friendship, SharedStudySet, User, StudySet, QuestionAnswer, Audio
from . import db
import smtplib
from email.message import EmailMessage
import webbrowser
import subprocess
from study_set_generator import generate_questions

views = Blueprint("views", __name__)
# views.static_url_path = '/static'

@views.route('/')  
def home():
    return render_template('home.html', user=current_user)

@views.route('/name')
def name():
    return render_template('name.html', user=current_user)

@views.route('/choose')
def choose():
    return render_template('choose.html', user=current_user)

@views.route('/dashboard')
def dashboard():
    return render_template('dashboard.html', user=current_user)

@views.route('/start_pygame_game')  # Define a route for starting the Pygame game
def start_pygame_game():
    try:
        # Execute the flashGame.py script
        subprocess.run(['python3', 'flashGame.py'], cwd='../Miss-Mangos-Class/FlashCardFiles')
        return 'Flash Cards started'
    except subprocess.CalledProcessError as e:
        return f'Error: {e}', 500

@views.route('/start_renpy_game')  # Define a route for starting the Ren'Py game
def start_renpy_game():
    # Logic to start Ren'Py game (replace with actual implementation)
    try:
        # Change directory to renpy-sdk and execute renpy.sh script
        subprocess.run(['/Users/reneecai/renpy-sdk/renpy.sh', '/Users/reneecai/Miss-Mangos-Class/RhythmGameFiles/renpy-rhythm-master 2'], check=True) 
        return 'Mango Beat started'
    except subprocess.CalledProcessError as e:
        return f'Error: {e}', 500
    
    ## The route that will take in stuff from HTML to generate the questions here:
@views.route('/generate_study_set', methods=['POST'])
def generate_study_set_route():
    # Call the study set generator function
    study_set = generate_questions()
    return jsonify(study_set)