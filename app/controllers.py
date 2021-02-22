from flask import url_for, redirect, request, render_template, Blueprint, session, flash
from flask_login import LoginManager
from app import app
from app.models import User

login_manager = LoginManager(app)

login_manager.login_view = 'index'



@login_manager.user_loader
def load_user(user_id):
    if user_id is not None:
        return User.query.get(user_id)
    return None

@login_manager.unauthorized_handler
def unauthorized():
    flash("You must login ")
    return redirect(url_for('index'))




@app.route('/')
def index():
    return render_template('index.html')
