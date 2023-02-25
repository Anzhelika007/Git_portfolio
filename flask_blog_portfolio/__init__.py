from flask import Flask


def create_app():
    print(__name__)
    app = Flask(__name__)
    return app
