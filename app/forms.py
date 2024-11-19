from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    PasswordField,
    BooleanField,
    SubmitField,
    FloatField,
    SelectField,
    DateField,
    IntegerField,
)
from wtforms.validators import (
    DataRequired,
    Email,
    EqualTo,
    ValidationError,
    NumberRange,
)
from app.models import User, PackageStatus


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


class CreatePackageForm(FlaskForm):
    tracking_number = StringField("Nyomkövetési szám", validators=[DataRequired()])
    status = SelectField(
        "Státusz",
        choices=[
            ("függőben", "Függőben"),
            ("szállítás alatt", "Szállítás alatt"),
            ("kézbesítve", "Kézbesítve"),
            ("visszaküldve", "Visszaküldve"),
        ],
        validators=[DataRequired()],
    )
    weight = FloatField("Súly (kg)", validators=[DataRequired(), NumberRange(min=0.1)])
    dimensions = StringField("Méretek (cm)", validators=[DataRequired()])
    sender_address = StringField("Feladó címe", validators=[DataRequired()])
    recipient_address = StringField("Címzett címe", validators=[DataRequired()])
    submit = SubmitField("Csomag létrehozása")


class EditPackageForm(FlaskForm):
    tracking_number = StringField("Nyomkövetési szám", validators=[DataRequired()])
    status = SelectField(
        "Státusz",
        choices=[
            ("függőben", "Függőben"),
            ("szállítás alatt", "Szállítás alatt"),
            ("kézbesítve", "Kézbesítve"),
            ("visszaküldve", "Visszaküldve"),
        ],
        validators=[DataRequired()],
    )
    weight = FloatField("Súly (kg)", validators=[DataRequired(), NumberRange(min=0.1)])
    sender_address = StringField("Feladó címe", validators=[DataRequired()])
    recipient_address = StringField("Címzett címe", validators=[DataRequired()])
    submit = SubmitField("Csomag módosítása")


class CreatePackageForm(FlaskForm):
    tracking_number = StringField("Nyomkövetési szám", validators=[DataRequired()])
    status = SelectField(
        "Státusz",
        choices=[(status, status) for status in PackageStatus.list()],
        validators=[DataRequired()],
    )
    weight = FloatField("Súly (kg)", validators=[DataRequired(), NumberRange(min=0.1)])
    dimensions = StringField("Méretek (cm)", validators=[DataRequired()])
    sender_address = StringField("Feladó címe", validators=[DataRequired()])
    recipient_address = StringField("Címzett címe", validators=[DataRequired()])
    delivery_deadline = DateField("Kézbesítési határidő", validators=[DataRequired()])
    submit = SubmitField("Csomag létrehozása")


class CreateWarehouseForm(FlaskForm):
    name = StringField("Név", validators=[DataRequired()])
    address = StringField("Cím", validators=[DataRequired()])
    capacity = IntegerField("Méret (mennyi csomag fér el összesen a raktárban)", validators=[DataRequired(), NumberRange(min=1)])
    current_load = IntegerField("Jelenlegi terhelés (mennyi csomag van a raktárban)", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Raktár létrehozása")


class EditWarehouseForm(FlaskForm):
    name = StringField("Név", validators=[DataRequired()])
    address = StringField("Cím", validators=[DataRequired()])
    capacity = IntegerField("Méret (mennyi csomag fér el összesen a raktárban)", validators=[DataRequired(), NumberRange(min=1)])
    current_load = IntegerField("Jelenlegi terhelés (mennyi csomag van a raktárban)", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Raktár módosítása")

class CreateParcelLockerForm(FlaskForm):
    location = StringField("Név", validators=[DataRequired()])
    address = StringField("Cím", validators=[DataRequired()])
    total_compartments = IntegerField("Méret (mennyi csomag fér el összesen a csomagautomatában)", validators=[DataRequired(), NumberRange(min=1)])
    available_compartments = IntegerField("Elérhető helyek (mennyi csomag fér még el csomagautomatában)", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Csomagautomata létrehozása")


class EditParcelLockerForm(FlaskForm):
    location = StringField("Név", validators=[DataRequired()])
    address = StringField("Cím", validators=[DataRequired()])
    total_compartments = IntegerField("Méret (mennyi csomag fér el összesen a csomagautomatában)", validators=[DataRequired(), NumberRange(min=1)])
    available_compartments = IntegerField("Elérhető helyek (mennyi csomag fér még el csomagautomatában)", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Csomagautomata módosítása")