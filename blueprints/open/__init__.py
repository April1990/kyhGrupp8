from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user

from models import User
from passlib.hash import argon2

# Create a blueprint object that can be used as an app object for this blueprint
bp_open = Blueprint('bp_open', __name__)


@bp_open.get('/')
def index():
    return render_template("index.html")


@bp_open.get('/login')
def login_get():
    return render_template('login.html')


@bp_open.post('/login')
def login_post():
    email = request.form['email']
    password = request.form['password']
    user = User.query.filter_by(email=email).first()
    if user is None:
        flash('Wrong email or password')
        return redirect(url_for('bp_open.login_get'))

    if not argon2.verify(password, user.password):
        flash('Wrong email or password')
        return redirect(url_for('bp_open.login_get'))

    # User is verified. Login in user!
    login_user(user)
    user.online = True

    from app import db
    db.session.commit()
    return redirect(url_for('bp_user.user_get'))


@bp_open.get('/signup')
def signup_get():
    return render_template('signup.html')


@bp_open.post('/signup')
def signup_post():
    name = request.form['name']
    email = request.form.get('email')
    public_rsa = request.form.get('public_rsa')
    password = request.form['password']
    hashed_password = argon2.using(rounds=10).hash(password)

    # Check if user with this password exists in the database
    user = User.query.filter_by(email=email).first()  # First will give us an object if user exist, or None if not
    if user:
        # If user is not none, then a user with this email exists in the database
        flash("Email address is already in use")
        return redirect(url_for('bp_open.signup_get'))

    new_user = User(name=name, email=email, password=hashed_password, public_rsa=public_rsa)

    from app import db
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for('bp_open.login_get'))