from flask import flash, render_template, redirect, url_for, Response
from flask_login import current_user, login_required, login_user, logout_user

from .forms import LoginForm, RegisterForm
from .models import User

from . import authentication


@authentication.route("/register", methods=["GET", "POST"])
def register_user() -> Response | str:
    # Check if user has already logged in
    if current_user.is_authenticated:
        flash("¡Ya has iniciado sesión!")
        return redirect(url_for("auth.homepage"))

    form = RegisterForm()

    # Create new user
    if form.validate_on_submit():
        User.create_user(
            user=form.name.data,
            email=form.email.data,
            password=form.password.data
        )
        flash("¡Usuario registrado!")
        return redirect(url_for("auth.user_log_in"))

    # Show main registration page if any error occurs
    return render_template("registration.html", form=form)


@authentication.route("/login", methods=["GET", "POST"])
def user_log_in() -> Response | str:
    # Check if user is already authenticated
    if current_user.is_authenticated:
        flash("¡Ya has iniciado sesión!")
        return redirect(url_for("auth.homepage"))

    form = LoginForm()
    if form.validate_on_submit():
        # Check if user is in database
        user: User = User.query.filter_by(user_email=form.email.data).first()

        if not user:
            flash("¡El usuario no existe!")
            return redirect(url_for("auth.user_log_in"))

        if not user.check_password(form.password.data):
            flash("¡La contraseña no es correcta!")
            return redirect(url_for("auth.user_log_in"))

        login_user(user, form.stay_logged.data)
        return redirect(url_for("auth.homepage"))

    return render_template("login.html", form=form)


@authentication.route("/logout", methods=["GET"])
@login_required
def log_out_user() -> Response:
    # Log out the user automatically
    logout_user()
    return redirect(url_for("auth.user_log_in"))


@authentication.route("/")
def index() -> str:
    return render_template("index.html")


@authentication.route("/homepage", methods=["GET"])
@login_required
def homepage() -> str:
    return render_template("homepage.html")


@authentication.errorhandler(404)
def page_not_found() -> str:
    return render_template("404_error.html")
