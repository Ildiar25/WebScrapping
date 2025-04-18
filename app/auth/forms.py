from flask_wtf import FlaskForm
from wtforms import BooleanField, Field, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from .models import User


def email_exists(form: FlaskForm, field: Field) -> bool | None:
    email = User.query.filter_by(user_email=field.data).first()
    if email:
        raise ValidationError("El email ya existe!")


class LoginForm(FlaskForm):
    email = StringField(
        label="Correo electrónico",
        validators=[
            DataRequired(),
            Email(),
        ]
    )
    password = PasswordField(
        label="Contraseña",
        validators=[
            DataRequired(),
        ]
    )
    stay_logged = BooleanField(
        label="Recuérdame"
    )
    submit = SubmitField(
        label="Iniciar Sesión"
    )


class RegisterForm(FlaskForm):
    name = StringField(
        label="Nombre",
        validators=[
            DataRequired(),
            Length(4, 16, message="El nombre debe tener entre 4 y 16 caracteres")
        ],
    )
    email = StringField(
        label="Correo electrónico",
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ]
    )
    password = PasswordField(
        label="Contraseña",
        validators=[
            DataRequired(),
            EqualTo("confirm_pw", message="Las contraseñas no coinciden")
        ]
    )
    confirm_pw = PasswordField(
        label="Repite la contraseña",
        validators=[
            DataRequired(),
            EqualTo("password", message="Las contraseñas no coinciden")
        ]
    )
    submit = SubmitField(
        label="Registrarse"
    )
