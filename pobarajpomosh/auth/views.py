"""
auth/views.py

Controller Responsible for Handling the auth pages

"""

from flask import render_template, redirect, url_for, abort, request, jsonify, flash
from flask_login import login_user, logout_user, current_user
from pobarajpomosh.auth import auth_bp
from pobarajpomosh.auth.models import User
from pobarajpomosh.auth.forms import LoginForm
from pobarajpomosh import db
from pobarajpomosh.decorators import check_valid_token, check_missing_fields
import uuid
from functools import wraps


@auth_bp.route('/api/login', methods=['POST'])
@check_missing_fields(["username", "password"])
def login():
    """
    <url>/auth/api/login

    View that returns a token when logged in succesfully

    """
    username = request.json.get('username').lower()
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()

    if user is None:
        return jsonify({"error": "Username or Password incorrect!"})

    if user.verify_password(password):
        token = str(uuid.uuid4().hex)
        user.token = token
        db.session.commit()
        return jsonify({"code": "success", 'token': token, "userId": user.id})

    return jsonify({"error": "Username or Password incorrect!"})


@auth_bp.route('/api/signup', methods=['POST'])
@check_missing_fields(["username", "password"])
def signup():
    """
    <url>/auth/api/signup

    View that signs up a user and returns a token

    """
    username = request.json.get('username').lower()
    password = request.json.get('password')
    if username is None or password is None:
        return jsonify({"error": "A Field is missing!"})

    user = User.query.filter_by(username=username).first()

    if user is not None:
        return jsonify({"error": "User already exists!"})

    token = str(uuid.uuid4().hex)
    user = User(username=username, role_id=4, approved=1, token=token)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'code': 'Registration Succesful!', 'token': token, "userId": user.id})


@auth_bp.route('/api/approve', methods=['POST'])
@check_missing_fields(["token", "user"])
@check_valid_token
def approve():
    """
    <url>/auth/api/approve

    View that approves a user

    """
    token = request.json.get('token')
    user = request.json.get('user')

    submitter = User.query.filter_by(token=token).first()

    # Who can Approve Users
    if submitter.role_id in [1, 2]:
        person = User.query.filter_by(id=user).first()
        if person is None:
            return jsonify({"error": "Invalid User"})
        person.approved += 1
        return jsonify({"code": "Approval Succesful!"})

    return jsonify({"code": "Access Denied!"})


@auth_bp.route('/login', methods=['GET', 'POST'])
def log_in():
    """
    url/auth/login

    Login via web
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for('volunteers.dashboard'))
        flash('Incorrect Email or Password!', 'alert-danger')
    return render_template('login.html', form=form)


@auth_bp.route("/logout", methods=['GET'])
def logout():
    """
    <url>/auth/logout

    A View which logs users out and redirects to the homepage

    """
    logout_user()
    flash('Logout Successful!', 'alert-success')
    return redirect(url_for('auth.log_in'))


@auth_bp.route("/api/user", methods=['POST'])
@check_missing_fields(["token", "user"])
def userinfo():
    """
    <url>/auth/api/user

    Get information about a user currently the username
    """
    token = request.json.get('token')
    user = request.json.get('user')

    if User.query.filter_by(token=token).first() is not None:
        username = User.query.filter_by(id=user).first()
        return jsonify({"username": username.username})

    return jsonify({"error": "Access Denied!"})


@auth_bp.route("/api/userinfo", methods=['POST'])
@check_valid_token
def usernamefromtoken():
    """
    <url>/auth/api/userinfo

    Get information about a user from a token
    """
    token = request.json.get('token')
    user = User.query.filter_by(token=token).first()

    return jsonify({"username": user.username})
