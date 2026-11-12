from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()

login_manager = LoginManager()

migrate = Migrate()

# Yahan hum extension objects create kar rahe hain. Inhe application factory mein initialize karenge.