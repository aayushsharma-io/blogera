from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
import os
import json
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    blogs = []
    blog_files = os.listdir('app/blogs')
    for filename in blog_files:
        with open(f'app/blogs/{filename}', 'r') as file:
            blog = json.load(file)
            blogs.append(blog)
    return render_template('index.html', blogs=blogs)

@bp.route('/blog/<blog_id>')
def blog_detail(blog_id):
    try:
        with open(f'app/blogs/{blog_id}.json', 'r') as file:
            blog = json.load(file)
        return render_template('blog_detail.html', blog=blog)
    except FileNotFoundError:
        flash('Blog not found.', 'danger')
        return redirect(url_for('main.index'))

@bp.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user_id = str(uuid.uuid4())
        new_user = {
            'id': user_id,
            'username': username,
            'password': password
        }
        with open('users.json', 'r') as file:
            users = json.load(file)
        users.append(new_user)
        with open('users.json', 'w') as file:
            json.dump(users, file)
        flash('Admin registered successfully!', 'success')
        return redirect(url_for('main.admin_login'))
    return render_template('admin_register.html')

@bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        with open('users.json', 'r') as file:
            users = json.load(file)
        for user in users:
            if user['username'] == username and user['password'] == password:
                user_obj = User(user['id'], user['username'], user['password'])
                login_user(user_obj)
                flash('Logged in successfully!', 'success')
                return redirect(url_for('main.admin'))
        flash('Invalid username or password.', 'danger')
    return render_template('admin_login.html')

@bp.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('main.index'))

@bp.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@bp.route('/admin/write', methods=['GET', 'POST'])
@login_required
def write_blog():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        content = request.form['content']
        thumbnail = request.files['thumbnail']
        thumbnail_filename = secure_filename(thumbnail.filename)
        thumbnail.save(os.path.join('app/static/uploads', thumbnail_filename))
        blog_id = str(uuid.uuid4())
        new_blog = {
            'id': blog_id,
            'title': title,
            'description': description,
            'content': content,
            'thumbnail': thumbnail_filename,
            'author': current_user.username,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        with open(f'app/blogs/{blog_id}.json', 'w') as file:
            json.dump(new_blog, file)
        flash('Blog post created successfully!', 'success')
        return redirect(url_for('main.admin'))
    return render_template('write_blog.html')

@bp.route('/blog/<blog_id>/add_comment', methods=['POST'])
@login_required
def add_comment(blog_id):
    comment = request.form['comment']
    try:
        with open(f'app/blogs/{blog_id}.json', 'r') as file:
            blog = json.load(file)
        if 'comments' not in blog:
            blog['comments'] = []
        blog['comments'].append({
            'author': current_user.username,
            'comment': comment,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })
        with open(f'app/blogs/{blog_id}.json', 'w') as file:
            json.dump(blog, file)
        flash('Comment added successfully!', 'success')
    except FileNotFoundError:
        flash('Blog not found.', 'danger')
    return redirect(url_for('main.blog_detail', blog_id=blog_id))
