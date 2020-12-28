from flask import url_for, redirect, request, render_template, Blueprint, session, flash
from flask.globals import current_app
from app.admin.models import User
from app.admin.forms import LoginForm, RegisterForm
from app import db

from app.admin import roles

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
def home():
    return render_template('admin/index.html')

@admin.route("/logout/")
def logout():
    session.pop('sid', None)
    flash("You have been logged out")
    return redirect(url_for('admin.home'))

@admin.route('/login/', methods=['GET', 'POST'])
def login():

    if "sid" in session:
        flash("Already Logged In")
        return redirect(url_for('admin.register'))

    if request.method == "POST":            

        form = LoginForm(request.form)

        user = User.query.filter_by(sid=form.sid.data).first()

        if user and user.password == form.password.data:
            session['sid'] = form.sid.data
            session['role'] = user.role
            flash("Login successful")
            return redirect(url_for("admin.register"))
        
        flash("Wrong ID or Password")
        
    form = LoginForm()       
    return render_template("admin/login.html",form= form)
    
        


@admin.route('/register/', methods=['GET', 'POST'])
def register():

    if not "sid" in session:
        flash("Not logged In")
        return redirect(url_for('admin.login'))
    
    current_user = {}
    current_user["sid"] = session['sid']
    current_user["role"] = roles[session['role']]
    

    if request.method == "POST":
        form = RegisterForm(request.form)

        user = User.query.filter_by(sid = form.sid.data).first()

        if not user and ( session['role'] < form.role.data or session['role'] == 1) :
            user = User(form.sid.data, form.password.data, form.role.data)
            db.session.add(user)
            db.session.commit()
            session['sid'] = form.sid.data
            flash("You Registered a User Succesfully")
            
        else:
            flash("Not Authorised or User already exists")    
    
    return render_template('admin/register.html', current_user=current_user)
   
        