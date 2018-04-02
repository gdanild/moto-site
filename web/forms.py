from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, StringField, PasswordField
from wtforms.validators import DataRequired, Length


class AddPostForm(FlaskForm):
    message = PasswordField("Пароль(не обязательно):  ")
    author =  StringField("Логин: ")
    google = StringField()
    submit = SubmitField("Отправить")
