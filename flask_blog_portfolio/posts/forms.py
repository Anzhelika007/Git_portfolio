from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired
from wtforms import SelectField
from flask_wtf.file import FileAllowed


class PostForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired()])
    content = TextAreaField('Текст', validators=[DataRequired()])
    picture = FileField('Приложите фото к посту', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Просмотр')


class CommentForm(FlaskForm):
    comment = StringField('Комментарий', validators=[DataRequired()])


class LikeForm(FlaskForm):
    submit = SubmitField('Создать')

