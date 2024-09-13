from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from app.models import User


class LoginForm(FlaskForm):
    username = StringField("Felhasználónév", validators=[DataRequired()])
    password = PasswordField("Jelszó", validators=[DataRequired()])
    remember_me = BooleanField("Emlékezz rám")
    submit = SubmitField("Bejelentkezés")


class RegistrationForm(FlaskForm):
    username = StringField("Felhasználónév", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Jelszó", validators=[DataRequired()])
    password2 = PasswordField(
        "Jelszó megerősítése", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Regisztráció")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Kérjük, használjon másik felhasználónevet.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Kérjük, használjon másik email címet.")
