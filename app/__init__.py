
import os

from flask import Flask

from config import Config
from .extensions import db, login_manager, migrate


def create_app():

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(Config)

    os.makedirs(app.instance_path, exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    from . import models
    from .models import User

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    migrate.init_app(app, db)

    login_manager.login_view = "auth.login"

    # Register blueprints
    from .auth.routes import auth_bp
    from .dashboard.routes import dashboard_bp
    from .urls.routes import urls_bp

    app.register_blueprint(
        auth_bp,
        url_prefix="/auth"
    )

    app.register_blueprint(
        dashboard_bp,
        url_prefix="/dashboard"
    )

    app.register_blueprint(urls_bp)

    return app
