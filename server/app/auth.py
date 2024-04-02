from flask import redirect, render_template, request, url_for, flash
# from flask_login import login_user, logout_user, login_required, current_user
from . import login_manager
from .models import User
from . import app
from . import login_user, logout_user, login_required, current_user

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        data = request.form.to_dict()
        user = User(name=data['name'],
                email=data['email'],
                password=data['password'],
                phone_no=data['phone_no'],
                gender=data['gender'],
                residence_location=data['residence_location'],
                residence_number=data['residence_number'],
                anonymity_level=data['anonymity_level'],
                theme_preference=data['theme_preference'],
                language_preference=data['language_preference'],
                notification_preference=data['notification_preference']
                )
        user.set_password(data['password'])
        user.save()
        return redirect(url_for('login'))
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form.to_dict()
        user = User.query.filter_by(email=data['email']).first()
        if user and user.check_password(data['password']):
            login_user(user)
            return redirect(url_for('home'))
        else:
            return "Invalid credentials", 401
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))