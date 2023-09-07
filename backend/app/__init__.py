import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager


# Initialize SQLAlchemy and Migrate instances without app context
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)

    # Configure database URL from environment variable
    database_url = os.environ.get('ALX_DB_URL')

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    print(database_url)

    # Configure secret key for jwt
    secret_key = os.environ.get('JWT_KEY')
    app.config['JWT_SECRET_KEY'] = secret_key
    print(secret_key)

    # Initialize db and migrate with the app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from .routes.auth import auth_bp
    from .routes.quiz import quiz_bp
    from .routes.admin import admin_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(quiz_bp, url_prefix='/quiz')
    app.register_blueprint(admin_bp, url_prefix='/admin')

    return app

from .models.categories import Category, Subcategory, Subject, Unit
from .models.question import Question
from .models.social import User, Comment, Attempt, MockSubject
