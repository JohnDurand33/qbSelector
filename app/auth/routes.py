from models import User, db, check_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, LoginManager, current_user, login_required
import helpers
from forms import SignInForm, SignUpForm

auth = Blueprint('auth', __name__, template_folder="auth_templates")

@auth.route('/signup', methods= ['GET', 'POST'])
def signup():
    form = SignUpForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            first_name = form.first_name.data or ''
            last_name = form.last_name.data or ''
            email = form.email.data
            password = form.password.data
            
            user = User(first_name=first_name, last_name=last_name, email=email, password=password)

            db.session.add(user)    
            db.session.commit()

    except:
        raise Exception('Invalid form data: please check your form')
    
    return render_template('sign_up.html', form=form, form_type='signup')

@auth.route('/signin', methods= ['GET', 'POST'])
def signin():
    form = SignInForm()

    try:
        if request.method == 'POST' and form.validate_on_submit():
            email = form.email.data
            password = form.password.data

            logged_user = User.query.filter(User.email == email).first()

            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                print(f"User {logged_user.email} logged in: {current_user.is_authenticated}")  # Debug print
                flash(f'You were successful in your login')
                return redirect(url_for('site.profile'))
            else:
                flash(f'You have failed to login (security!)', 'error')
                return redirect(url_for('auth.signin'))
    except:
        raise Exception('Invalid form data: Please check your form')

    return render_template('sign_in.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('site.home'))