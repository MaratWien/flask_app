from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from . import db
from .models import Post


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)


@main.route('/blog', methods=['POST', 'GET'])
def blog():
    posts = db.session.query(Post)

    return render_template('blog.html', posts=posts)


@main.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')

        if not title:
            flash('Title is required!')
        else:
            new_post = Post(title=title, content=content)

            db.session.add(new_post)
            db.session.commit()

            return redirect(url_for('main.blog'))

    return render_template('create.html')


@main.route('/delete', methods=['POST'])
def delete():
    post_id = request.url.split('=')[-1]

    Post.query.filter_by(id=post_id).delete()

    db.session.commit()

    # posts = db.session.query(Post)
    # return render_template('blog.html', posts=posts)
    return redirect(url_for('main.blog'))


