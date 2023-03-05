from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from flask_login import current_user, login_required
from flask_blog_portfolio import db
from flask_blog_portfolio.models import Post, Comment, Like, Category, Hashtag, hashtag_posts
from flask_blog_portfolio.posts.forms import PostForm, CommentForm, LikeForm
from flask_blog_portfolio.users.utils import save_picture

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    posts_first = Post.query.order_by(Post.date_posted.desc()).first_or_404()
    posts = Post.query.order_by(Post.date_posted.desc()).all()
    categories = Category.query.all()

    for i in categories:
        count = Post.query.filter_by(category_id=i.id).count()
        print(i.name, count)
    print(categories)
    print(posts_first.title)
    return render_template('home.html', posts_first=posts_first, categories=categories, posts=posts)
