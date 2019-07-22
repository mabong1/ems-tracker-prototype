import sys, os

sys.path.insert(0, os.path.join(
    os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'application'))
from flask import Flask
from views import tracker
from flask_webpack_loader import WebpackLoader

# Initiate the Flask application
app = Flask(__name__)

# Configure Flask configuration
app.config.from_object('config')
app.config.from_pyfile('config.py')
app.register_blueprint(tracker)

# Configure webpack loader
webpack_loader = WebpackLoader(app)
