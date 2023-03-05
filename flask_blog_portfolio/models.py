from datetime import datetime, timedelta, timezone
from flask_blog_portfolio import db, login_manager
from flask_login import UserMixin
from jwt import encode, decode
from flask import current_app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    post = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"Пользователь('{self.username}', '{self.email}', '{self.image_file}')"

    def get_reset_token(self, expires_sec=1800):
        payload = {'user_id': self.id,
                   'exp': datetime.now(timezone.utc) + timedelta(
                       seconds=expires_sec)}
        return encode(payload, current_app.config['SECRET_KEY'], algorithm="HS256")

    @staticmethod
    def verify_reset_token(token, leeway=10):
        """десериализация ключа"""
        try:
            data = decode(token, current_app.config['SECRET_KEY'], leeway=leeway, algorithms=['HS256'])
        except Exception:
            return None
        return User.query.get(data['user_id'])


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return '<Category %r>' % self.name


hashtag_posts = db.Table('hashtag_article',
                           db.Column('hashtag_id', db.Integer, db.ForeignKey('hashtag.id')),
                           db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
                           )


class Hashtag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return '<Hashtag %r>' % self.name

    def __str__(self):
        return self.name


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    update_post = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    hashtags = db.relationship('Hashtag', secondary=hashtag_posts, backref=db.backref('posts', lazy='dynamic'))

    comments = db.relationship('Comment', backref='title', lazy='select', cascade='all, delete-orphan')

    def __repr__(self):
        return f"Запись('{self.title}', '{self.date_posted}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    username = db.Column(db.String, db.ForeignKey('user.username'), nullable=False)


class Like(db.Model):
    __table_args__ = (db.PrimaryKeyConstraint('user_id', 'post_id', name='CompositePkForLike'),)

    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.String(36), db.ForeignKey('post.id'), nullable=False)



