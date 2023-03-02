from flask_blog_portfolio import create_app
from flask_blog_portfolio import db


app = create_app()
app.app_context().push()
db.create_all()
