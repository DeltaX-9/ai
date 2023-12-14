# app/src/graph/routes.py
from flask import Blueprint, render_template

flask_app = Blueprint('src.graph', __name__)

@flask_app.route('/')
def index():
    return "helllo world"

# @flask_app.route('/about')
# def about():
#     return render_template('main/about.html')
