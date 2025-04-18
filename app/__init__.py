import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

from .auth import authentication


def create_app(config_type: str) -> Flask:

    # Create app and set configs
    app = Flask(__name__)
    settings = os.path.join(os.getcwd(), "config", config_type + ".py")
    app.config.from_pyfile(settings)

    # Initialize database
    db.init_app(app)

    # Initialize styles
    bootstrap.init_app(app)

    # Initialize login management
    login_manager.init_app(app)

    # Initialize encryption data
    bcrypt.init_app(app)

    # Register blueprint
    app.register_blueprint(authentication)

    return app


def create_login_manager() -> LoginManager:
    log_manager = LoginManager()
    log_manager.login_view = "auth.user_log_in"
    log_manager.session_protection = "strong"
    return log_manager


# Initialize models
db = SQLAlchemy()
bootstrap = Bootstrap()
bcrypt = Bcrypt()
login_manager = create_login_manager()

from .auth import views as views  # Improve Circular Import... Needs to be loaded to see templates
