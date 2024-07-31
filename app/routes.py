import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
from flask_login import login_required, current_user
import json
from datetime import datetime

bp = Blueprint('main', __name__)

def save_file(file):
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + '_' + file.filename
    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    return filename

@bp.route('/')
def index():
    blogs = []
    if os.path.exists('app/blogs'):
        for filename in os.listdir('app/blogs'):
            if filename.endswith('.json'):
                with open(os.path.join('app/blogs', filename), 'r') as f:
                    blogs.append(json.load(f))
    return render_template('index.html', blogs=blogs)

@bp.route('/blog/<blog_id>')
def blog_detail(blog_id):
    blog_file = f'app/blogs/{blog_id}.json'
    if not os.path.exists(blog_file):
        abort(404)
    with open(blog_file, 'r') as f:
        blog = json.load(f)
    return render_template('blog_detail.html', blog=blog)

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
        thumbnail_file = request.files['thumbnail']
        allow_comments = 'allow_comments' in request.form

        if not title or not description or not content:
            flash('Title, description, and content are required.')
            return redirect(url_for('main.write_blog'))

        if thumbnail_file:
            thumbnail_filename = save_file(thumbnail_file)
        else:
            flash('Thumbnail is required.')
            return redirect(url_for('main.write_blog'))

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        blog_id = f'blog{datetime.now().strftime("%Y%m%d%H%M%S")}'
        blog_data = {
            'id': blog_id,
            'title': title,
            'description': description,
            'content': content,
            'thumbnail': url_for('static', filename=f'uploads/{thumbnail_filename}'),
            'allow_comments': allow_comments,
            'author': current_user.username,
            'timestamp': timestamp
        }

        if not os.path.exists('app/blogs'):
            os.makedirs('app/blogs', exist_ok=True)

        with open(f'app/blogs/{blog_id}.json', 'w') as f:
            json.dump(blog_data, f)

        flash('Blog post created successfully.')
        return redirect(url_for('main.index'))

    return render_template('write_blog.html')

@bp.route('/blog/<blog_id>/add_comment', methods=['POST'])
def add_comment(blog_id):
    blog_file = f'app/blogs/{blog_id}.json'
    if not os.path.exists(blog_file):
        abort(404)
    with open(blog_file, 'r+') as f:
        blog = json.load(f)
        comment = {
            'author': current_user.username if current_user.is_authenticated else 'Anonymous',
            'content': request.form['comment'],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        if 'comments' not in blog:
            blog['comments'] = []
        blog['comments'].append(comment)
        f.seek(0)
        json.dump(blog, f)
    return redirect(url_for('main.blog_detail', blog_id=blog_id))
