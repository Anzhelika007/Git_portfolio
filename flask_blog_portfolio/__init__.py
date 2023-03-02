from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_blog_portfolio.config import Config
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_migrate import Migrate

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    migrate = Migrate(app, db)

    from flask_blog_portfolio.main.routes import main
    from flask_blog_portfolio.users.routes import users
    from flask_blog_portfolio.posts.routes import posts
    from flask_blog_portfolio.errors.routes import errors

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app
