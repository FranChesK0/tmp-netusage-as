from flask_wtf import FlaskForm
from wtforms import BooleanField, DateField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError

from app.models import User


class UserForm(FlaskForm):
    username = StringField("Имя пользователя", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    is_admin = BooleanField("Администратор?")
    submit = SubmitField("Создать пользователя")

    def validate_username(self, field):
        user = User.query.filter_by(username=field.data).first()
        if user is not None:
            raise ValidationError("Используйте другое имя пользователя.")

    def validate_email(self, field):
        user = User.query.filter_by(email=field.data).first()
        if user is not None:
            raise ValidationError("Используйте другой адрес почты.")


class DateForm(FlaskForm):
    start = DateField("От", validators=[DataRequired()])
    end = DateField("До", validators=[DataRequired()])
    submit = SubmitField("Загрузить")
