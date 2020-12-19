from flask import url_for, redirect, request, render_template, Blueprint, session
from app.admin.models import User
from app.admin.forms import LoginForm, RegisterForm
from app import db

admin = Blueprint('admin', __name__, url_prefix='/admin')

@admin.route('/home/')
def home():
    form = LoginForm()
    return render_template('admin/index.html',form=form)

@admin.route('/login/', methods=['GET', 'POST'])
def login():

    if request.method == "POST":
        form = LoginForm(request.form)
        if form.validate_on_submit():
            user = User.query.filter_by(sid=form.sid.data).first()
            if user and user.password == form.password.data:
                session['sid'] = user.sid
                session['role'] = user.role
            
                return "Login Successfull"
            return "Email or password wrong!"
    
    form = LoginForm()
    return render_template('admin/index.html', form=form)
        
@admin.route('/register/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():

        user_role = int(form.role)
        current_role = session['role']

        if user_role < 1 or user_role > 3:
            return "Role is not in bounds"

        if current_role >= user_role:
            return "Access Failure"

        if db.session.query(exists().where(User.sid == form.sid.data)):
            return "User already exists"

        user = User(form.sid.data, form.password.data, form.role.data)
        db.session.add(user)
        db.session.commit()
        return "User has been added"
        

    return render_template(url_for('admin/register.html', form=form))