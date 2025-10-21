from flask import Flask
from config import Config
from extensions import db, migrate, bcrypt
from app import models  # imports all models

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Register blueprints

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
