from flask import Flask

# Create Flask application
app = Flask(__name__)
app.config.from_pyfile('config.py')