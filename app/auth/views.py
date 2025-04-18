import requests
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from flask import flash, render_template, redirect, url_for, Response
from flask_login import current_user, login_required, login_user, logout_user
from lxml import etree

from .forms import LoginForm, RegisterForm, ScrapyForm
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


@authentication.route("/scrapy_data", methods=["GET", "POST"])
@login_required
def scrapy_data() -> str:
    form = ScrapyForm()

    if form.validate_on_submit():
        new_category = form.new_category.data
        base_url = "https://books.toscrape.com/catalogue/category/books/nothing_to_see/"

        # Get BooksToScrape response with the category
        response = requests.get(f"https://books.toscrape.com/catalogue/category/books/{new_category}/index.html")

        # Get full HTML page
        soup = BeautifulSoup(response.content, "html.parser")

        # Get all URL items
        html_tree = etree.HTML(str(soup))
        relative_links = html_tree.xpath("//article[@class='product_pod']//h3//a/@href")

        # Get URL absolutes
        absolute_urls = [urljoin(base_url, link) for link in relative_links]
        return render_template("scrapy_data.html", links=absolute_urls)

    return render_template("scrapy_data.html", form=form)


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


@authentication.app_errorhandler(404)
def page_not_found(error) -> str:
    return render_template("404_error.html", error=error)
