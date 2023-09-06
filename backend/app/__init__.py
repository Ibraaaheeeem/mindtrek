import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize SQLAlchemy and Migrate instances without app context
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Configure database URL from environment variable
    database_url = os.environ.get('ALX_DB_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    # Initialize db and migrate with the app
    db.init_app(app)
    migrate.init_app(app, db)

    return app
