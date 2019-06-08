"""
main/views.py

Controller Responsible for Handling the main page

"""

from flask import render_template
from pobarajpomosh.main import main_bp


@main_bp.route('/')
def homepage():
    """
    <url>/

    View that Renders the Homepage

    """
    return render_template('index.html')


@main_bp.route('/gostuvanja')
def mediapage():
    """
    <url>/

    View that Renders Press Stuff

    """
    return render_template('gostuvanja.html')
