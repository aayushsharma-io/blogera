from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .forms import LoginForm, RegisterForm
from .models import User
import json
import os

auth = Blueprint('auth', __name__)

@auth.route('/admin/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = generate_password_hash(form.password.data, method='sha256')

        if not os.path.exists('app/data/users.json'):
            os.makedirs('app/data', exist_ok=True)
            with open('app/data/users.json', 'w') as f:
                json.dump([], f)

        with open('app/data/users.json', 'r+') as f:
            users = json.load(f)
            if any(user['username'] == username for user in users):
                flash('Username already exists.')
                return redirect(url_for('auth.register'))
            users.append({'id': len(users) + 1, 'username': username, 'password': password})
            f.seek(0)
            json.dump(users, f)

        flash('Account created successfully.')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        if not os.path.exists('app/data/users.json'):
            flash('No users found. Please register first.')
            return redirect(url_for('auth.register'))

        with open('app/data/users.json', 'r') as f:
            users = json.load(f)
            user = next((u for u in users if u['username'] == username), None)
            if user and check_password_hash(user['password'], password):
                user_obj = User(user['id'], user['username'])
                login_user(user_obj)
                return redirect(url_for('main.admin'))
            else:
                flash('Invalid username or password.')

    return render_template('login.html', form=form)

@auth.route('/admin/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
