import os
from flask import Flask, render_template
import subprocess

app = Flask(__name__)
app.static_url_path = '/static'

@app.route('/')  
def home():
    return render_template('home.html')

@app.route('/name')
def name():
    return render_template('name.html')

@app.route('/choose')
def choose():
    return render_template('choose.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/start_pygame_game')  # Define a route for starting the Pygame game
def start_pygame_game():
    try:
        # Execute the flashGame.py script
        subprocess.run(['python3', 'flashGame.py'], cwd='/Users/reneecai/Miss-Mangos-Class/FlashCardFiles')
        return 'Flash Cards started'
    except subprocess.CalledProcessError as e:
        return f'Error: {e}', 500

@app.route('/start_renpy_game')  # Define a route for starting the Ren'Py game
def start_renpy_game():
    # Logic to start Ren'Py game (replace with actual implementation)
    try:
        # Change directory to renpy-sdk and execute renpy.sh script
        subprocess.run(['/Users/reneecai/renpy-sdk/renpy.sh', '/Users/reneecai/Miss-Mangos-Class/RhythmGameFiles/renpy-rhythm-master 2'], check=True) 
        return 'Mango Beat started'
    except subprocess.CalledProcessError as e:
        return f'Error: {e}', 500

if __name__ == '__main__':
    app.run(debug=True) 