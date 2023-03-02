from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_blog_portfolio.models import User, Post
from flask_blog_portfolio import db
from flask_blog_portfolio import create_app

app = create_app()

admin = Admin(app)
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
