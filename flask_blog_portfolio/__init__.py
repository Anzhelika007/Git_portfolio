from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_blog_portfolio.config import Config

db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    db.init_app(app)

    #Application Registration
    from flask_blog_portfolio.main.routes import main
    app.register_blueprint(main)

    app.config.from_object(Config)

    return app
