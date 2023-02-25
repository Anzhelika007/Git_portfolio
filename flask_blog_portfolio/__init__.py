from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_blog_portfolio.config import Config
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from flask_blog_portfolio.main.routes import main
    from flask_blog_portfolio.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)

    app.config.from_object(Config)

    return app
