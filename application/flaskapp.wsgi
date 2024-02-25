import sys

# Adjust the following line to the path where your Flask app is located
sys.path.insert(0, '/home/ubuntu/source/csc648-sp24-03-team04/application')

# Import the Flask app object. Adjust 'application' to match the name of your Flask app.
# For example, if your main file is app.py and it contains a Flask application object
# named 'app', then it would be 'from application.app import app as application'
from app import app as application
